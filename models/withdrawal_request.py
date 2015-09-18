from decorators import *
from H2O.settings import DEBUG
from models.exceptions import NotEnoughMoneyException, InvalidEmail
from models import User, Transaction, UserAccount

import json
import random
import string

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class WithdrawalRequest:
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
        provider_transaction_id = ''.join(random.choice(string.ascii_uppercase) for i in range(12))


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


    @staticmethod
    @raw_queries()
    def do_real_withdrawal(user_id, provider, email, amount, currency, db):
        amount = float(amount)
        user = User.get_by_id(user_id, scope='all_with_balance')
        user_uuid = user['uuid']
        user_balance = user['balance']

        if user_balance < amount:
            raise NotEnoughMoneyException()

        sender_batch_id = provider_transaction_id = ''

        from paypalrestsdk import Payout
        try:
            payout = Payout({
                "sender_batch_header": {
                    "sender_batch_id": sender_batch_id,
                    "email_subject": "You have a payment"
                },
                "items": [
                    {
                        "recipient_type": "EMAIL",
                        "amount": {
                            "value": amount,
                            "currency": "USD"
                        },
                        "receiver": email,
                        "note": "We pay you.",
                        "sender_item_id": "item_1"
                    }
                ]
            })

            if payout.create(sync_mode=True):
                logger.info(payout)
            else:
                raise Exception(payout.error)

            payout = payout['items'][0]

            if not DEBUG and payout['transaction_status'] != 'SUCCESS':
                raise NotAcceptableException()

        except Exception, e:
            logger.warn(e)
            raise

        # write to db
        with db.t():
            # transaction

            transaction_id = Transaction.add_withdrawal_db(
                db,
                user_id, user_uuid,
                amount, currency,
                'paypal', sender_batch_id,
                email, payout
            )

            # increase balance
            UserAccount.update_user_balance(db, user_id, -amount, currency)

        # update statistics sync.
        # TODO: make it async.
        from models.statistics import Statistics
        Statistics.update_statistics_via_transaction(user_id, transaction_id)

        #
        return transaction_id


