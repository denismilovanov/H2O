from decorators import *
from H2O.settings import DEBUG
from models.exceptions import NotEnoughMoneyException, InvalidEmail, NotImplementedException
from models import User, Transaction, UserAccount

import json
import random
import string

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class WithdrawalRequest:
    @staticmethod
    def get_random_provider_transaction_id(provider):
        if provider == 'paypal':
            return ''.join(random.choice(string.ascii_uppercase) for i in range(12))
        raise NotImplementedException()

    @staticmethod
    def scope(scope):
        if scope == 'public':
            return ', '.join(['id', 'amount', 'currency', 'status'])
        else:
            return '*'

    @staticmethod
    @raw_queries()
    def get_withdrawal_requests_by_user_id(user_id, limit, offset, db):
        return db.select_table('''
            SELECT  ''' + WithdrawalRequest.scope('public') + ''',
                    public.format_datetime(created_at) AS created_at,
                    public.format_datetime(billed_at) AS billed_at
                FROM billing.get_withdrawal_requests_by_user_id(%(user_id)s, %(limit)s, %(offset)s);
        ''', user_id=user_id, limit=limit, offset=offset)

    @staticmethod
    @raw_queries()
    def get_withdrawal_requests_by_id(user_id, request_id, db):
        request = db.select_record('''
            SELECT ''' + WithdrawalRequest.scope('all') + '''
                FROM billing.get_withdrawal_request_by_id(%(user_id)s, %(request_id)s);
        ''', user_id=user_id, request_id=request_id)

        if not request['id']:
            return None

        return request

    @staticmethod
    @raw_queries()
    def update_withdrawal_request(user_id, request_id, status,
                                  request_data, response_data, our_transaction_id, db):
        db.select_field('''
            SELECT billing.update_withdrawal_request(
                %(user_id)s, %(request_id)s,
                %(status)s, %(request_data)s, %(response_data)s,
                %(our_transaction_id)s
            );
        ''',
            user_id=user_id, request_id=request_id, status=status,
            request_data=json.dumps(request_data), response_data=json.dumps(response_data),
            our_transaction_id=our_transaction_id
        )

    @staticmethod
    @raw_queries()
    def add_withdrawal_request(user_id, amount, currency, provider, data, db):
        amount = float(amount)

        email = None
        if provider == 'paypal':
            email = data['email']
            from validate_email import validate_email
            if not email or not validate_email(email):
                raise InvalidEmail()

        user = User.get_by_id(user_id, scope='all_with_balance')
        user_uuid = user['uuid']
        user_balance = user['balance']

        # check balance
        if user_balance < amount:
            raise NotEnoughMoneyException()

        # unique transaction id
        provider_transaction_id = WithdrawalRequest.get_random_provider_transaction_id(provider)

        #
        with db.t():
            # insert into db
            withdrawal_request_id = db.select_field('''
                SELECT billing.add_withdrawal_request(
                    %(user_id)s, %(user_uuid)s,
                    %(amount)s, %(currency)s,
                    %(provider)s, %(provider_transaction_id)s,
                    %(email)s, %(data)s
                );
            ''',
                user_id=user_id, user_uuid=user_uuid, amount=amount, currency=currency,
                provider=provider, provider_transaction_id=provider_transaction_id,
                data=json.dumps(data), email=email
            )

            # decrease balance, increase hold money
            new_balance = UserAccount.update_user_balance(db, user_id, -amount, currency, amount)
            if new_balance < 0:
                raise NotEnoughMoneyException()

        if not withdrawal_request_id:
            raise Exception('Generated transaction id is not unique.')

        # perform w/d async
        from tasks.perform_withdrawal_request_task import PerformWithdrawalRequestTask
        PerformWithdrawalRequestTask(user_id, withdrawal_request_id).enqueue()

        #
        return withdrawal_request_id


    @staticmethod
    @raw_queries()
    def perform_withdrawal_request(user_id, request_id, db):
        # user and his data
        user = User.get_by_id(user_id, scope='all_with_balance')
        user_uuid = user['uuid']
        user_hold = user['hold']

        # request and its data
        request = WithdrawalRequest.get_withdrawal_requests_by_id(user_id, request_id)
        if not request:
            raise Exception('There is no request')

        if request['provider'] != 'paypal':
            raise NotImplementedException()

        provider_transaction_id = request['provider_transaction_id']
        amount = float(request['amount'])
        currency = request['currency']
        provider = request['provider']
        email = None
        if provider == 'paypal':
            email = request['email']

        # check hold
        if user_hold < amount:
            raise NotEnoughMoneyException()

        # check debug
        if DEBUG:
            # to prevent 'Duplicate batch request'
            provider_transaction_id = WithdrawalRequest.get_random_provider_transaction_id(provider)

        # perform
        success = False
        request_data = response_data = None

        from paypalrestsdk import Payout
        try:
            request_data = {
                "sender_batch_header": {
                    "sender_batch_id": provider_transaction_id,
                    "email_subject": "You have a payment from H2O"
                },
                "items": [
                    {
                        "recipient_type": "EMAIL",
                        "amount": {
                            "value": amount,
                            "currency": currency.upper(),
                        },
                        "receiver": email,
                        "note": "Payment from H2O",
                        "sender_item_id": "item_1"
                    }
                ]
            }

            # perform sync request with this data
            logger.info(request_data)
            payout = Payout(request_data)

            if payout.create(sync_mode=True):
                logger.info(payout)
            else:
                response_data = payout.error
                raise Exception(payout.error)

            # the single payout in batch
            payout = payout['items'][0]

            # check status
            if not DEBUG:
                success = payout['transaction_status'] == 'SUCCESS'
            else:
                success = payout['transaction_status'] == 'UNCLAIMED'

            # response is payout itself
            response_data = str(payout)

        except Exception, e:
            # any exception causes status 'failed'
            success = False

            # notify developer
            from tasks.send_exception_task import SendExceptionTask
            SendExceptionTask(e).enqueue()

        #
        logger.info(success)
        logger.info(response_data)

        # write to db
        with db.t():
            our_transaction_id = None

            if success:
                # w/d transaction in our system
                our_transaction_id = Transaction.add_withdrawal_db(
                    db,
                    user_id, user_uuid,
                    amount, currency,
                    provider, provider_transaction_id
                )

                # decrease hold
                UserAccount.update_user_balance(db, user_id, +0, currency, -amount)

            # remember response in any case
            WithdrawalRequest.update_withdrawal_request(
                user_id, request_id,
                'success' if success else 'failed',
                request_data, response_data,
                our_transaction_id
            )


        if success:
            # update statistics sync.
            # TODO: make it async.
            from models.statistics import Statistics
            Statistics.update_statistics_via_transaction(user_id, our_transaction_id)

        return True

