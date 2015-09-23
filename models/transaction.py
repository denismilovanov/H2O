from decorators import *
from models import User, UserFollow, UserAccount
from models.exceptions import ResourceIsNotFound, ConflictException, NotAcceptableException, NotEnoughMoneyException

import json

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Transaction:
    @staticmethod
    def scope(scope):
        if scope == 'public':
            return ', '.join(['id', 'amount', 'currency', 'status', 'direction', 'user_uuid', 'counter_user_uuid', 'is_anonymous'])
        else:
            return '*'

    @staticmethod
    def get_transactions_by_dates_raw(users_ids, from_date, to_date, direction, db):
        return db.select_table('''
            SELECT ''' + Transaction.scope('public') + ''',
                    public.format_datetime(created_at) AS created_at,
                    counter_user_id, user_id
                FROM billing.get_transactions_by_users_ids_and_dates(%(users_ids)s, %(from_date)s::date, %(to_date)s::date, %(direction)s);
        ''', users_ids=users_ids, from_date=from_date, to_date=to_date, direction=direction)

    @staticmethod
    def get_transactions_by_offset_raw(users_ids, limit, offset, exclude_counter_users_ids, db):
        return db.select_table('''
            SELECT ''' + Transaction.scope('public') + ''',
                    public.format_datetime(created_at) AS created_at,
                    counter_user_id, user_id
                FROM billing.get_transactions_by_users_ids_and_offset(
                    %(users_ids)s, %(limit)s, %(offset)s, %(exclude_counter_users_ids)s
                );
        ''',
            users_ids=users_ids, limit=limit, offset=offset,
            exclude_counter_users_ids=exclude_counter_users_ids
        )

    @staticmethod
    @raw_queries()
    def get_transaction_by_id(user_id, transaction_id, db):
        transaction = db.select_record('''
            SELECT ''' + Transaction.scope('all') + '''
                FROM billing.get_transaction_by_id(%(user_id)s, %(transaction_id)s);
        ''', user_id=user_id, transaction_id=transaction_id)

        if not transaction['id']:
            return None

        return transaction

    @staticmethod
    def get_users_ids(whose, user_id):
        users_ids = []

        if whose == 'my':
            # all transactions of me
            users_ids = [user_id]
        elif whose == 'follows':
            # my follows
            users_ids = UserFollow.get_user_follows_ids(user_id)

        return users_ids

    @staticmethod
    @raw_queries()
    def get_transactions_by_dates(user_id, whose, direction, from_date, to_date, db):
        #
        users_ids = Transaction.get_users_ids(whose, user_id)

        # all transactions of them
        transactions = Transaction.get_transactions_by_dates_raw(users_ids, from_date, to_date, direction, db)

        #
        return Transaction.prepare_transactions_response(transactions, whose, user_id)


    @staticmethod
    @raw_queries()
    def get_transactions_by_offset(user_id, whose, limit, offset, db):
        #
        users_ids = Transaction.get_users_ids(whose, user_id)

        # exclude me as counter from my follows transactions
        exclude_counter_users_ids = None
        if whose == 'follows':
            exclude_counter_users_ids = [user_id]

        # all transactions of them
        transactions = Transaction.get_transactions_by_offset_raw(users_ids, limit, offset, exclude_counter_users_ids, db)

        #
        return Transaction.prepare_transactions_response(transactions, whose, user_id)

    @staticmethod
    def prepare_transactions_response(transactions, whose, user_id):
        # collect participants ids
        participants_users_ids = []

        # remove some indeces
        # perform some transformation depending on circumstances
        for transaction in transactions:

            # add counter_user_id to participants_users_ids

            if transaction['direction'] == 'receive' and transaction['is_anonymous']:
                # anonymous receives
                transaction['counter_user_uuid'] = None
            elif transaction['counter_user_id'] != user_id:
                # public receives
                participants_users_ids.append(transaction['counter_user_id'])

            # add user_id to participants_users_ids

            if whose == 'me':
                if transaction['user_id'] != user_id:
                    participants_users_ids.append(transaction['user_id'])

            elif whose == 'follows':
                if transaction['direction'] == 'support' and transaction['is_anonymous']:
                    transaction['user_uuid'] = None
                elif transaction['user_id'] != user_id:
                    participants_users_ids.append(transaction['user_id'])

            # no need to output this
            del transaction['counter_user_id']
            del transaction['user_id']

        # uniq
        participants_users_ids = list(set(participants_users_ids))

        # gather all
        result = {
            'transactions': transactions,
            'users': User.get_all_by_ids(participants_users_ids, scope='public_profile_with_i_follow', viewer_id=user_id),
        }

        # we are ready!
        return result

    @staticmethod
    def add_transaction_raw(db, user_id, user_uuid, counter_user_id, counter_user_uuid, direction,
                            amount, currency, is_anonymous):

        return db.select_field('''
            SELECT billing.add_transaction(
                %(user_id)s, %(user_uuid)s,
                %(counter_user_id)s, %(counter_user_uuid)s,
                %(direction)s, %(amount)s, %(currency)s, %(is_anonymous)s,
                NULL, NULL
            );
        ''',
            user_id=user_id, user_uuid=user_uuid,
            counter_user_id=counter_user_id, counter_user_uuid=counter_user_uuid,
            direction=direction,
            amount=amount, currency=currency, is_anonymous=is_anonymous
        )

    @staticmethod
    def add_deposit_db(db, user_id, user_uuid, amount, fee, currency,
                        provider, provider_transaction_id):

        return db.select_field('''
            SELECT billing.add_transaction(
                %(user_id)s, %(user_uuid)s,
                NULL, NULL,
                'deposit', %(amount)s, %(currency)s, FALSE,
                %(provider)s, %(provider_transaction_id)s,
                %(fee)s
            );
        ''',
            user_id=user_id, user_uuid=user_uuid,
            amount=amount, currency=currency,
            provider=provider, provider_transaction_id=provider_transaction_id,
            fee=fee
        )

    @staticmethod
    def add_withdrawal_db(db, user_id, user_uuid, amount, currency, provider, provider_transaction_id):
        return db.select_field('''
            SELECT billing.add_transaction(
                %(user_id)s, %(user_uuid)s,
                NULL, NULL,
                'withdraw', %(amount)s, %(currency)s, FALSE,
                %(provider)s, %(provider_transaction_id)s
            );
        ''',
            user_id=user_id, user_uuid=user_uuid,
            amount=amount, currency=currency,
            provider=provider, provider_transaction_id=provider_transaction_id
        )

    @staticmethod
    @raw_queries()
    def add_support(user_id, counter_user_id, amount, currency, is_anonymous, db):
        amount = float(amount)
        user = User.get_by_id(user_id, scope='all_with_balance')
        user_uuid = user['uuid']
        user_balance = user['balance']

        if user_balance < amount:
            raise NotEnoughMoneyException()

        counter_user_uuid = User.get_by_id(counter_user_id, scope='all')['uuid']

        try:
            with db.t():
                # support
                transaction_id = Transaction.add_transaction_raw(
                    db,
                    user_id, user_uuid,
                    counter_user_id, counter_user_uuid,
                    'support',
                    amount, currency, is_anonymous
                )

                # decrease balance
                new_balance = UserAccount.update_user_balance(db, user_id, -amount, currency)

                # check balance again
                # it is actual because between selecting and updating balance there is small time gap
                #
                # Trans1 ----- SELECT balance ------- UPDATE balance
                # Trans2 --------- SELECT balance -------- UPDATE balance (will wait and then return negative)
                #
                if new_balance < 0:
                    raise NotEnoughMoneyException()

                # receive
                counter_transaction_id = Transaction.add_transaction_raw(
                    db,
                    counter_user_id, counter_user_uuid,
                    user_id, user_uuid,
                    'receive',
                    amount, currency, is_anonymous
                )

                # increase balance
                UserAccount.update_user_balance(db, counter_user_id, +amount, currency)

        except Exception, e:
            raise e

        # update statistics sync.
        # TODO: make it async.
        from models.statistics import Statistics
        Statistics.update_statistics_via_transaction(user_id, transaction_id)
        Statistics.update_statistics_via_transaction(counter_user_id, counter_transaction_id)

        # sending notification though queue
        try:
            from tasks.notify_support_task import NotifySupportTask
            # counter_user_id will receive notification
            # user_id will become counter_user_id inside NotifySupportTask
            NotifySupportTask(counter_user_id, user_id, amount, currency, is_anonymous).enqueue()
        except Exception, e:
            # there is no need to raise exception and scare user
            logger.info(e)

        return transaction_id

    @staticmethod
    @raw_queries()
    def add_deposit(user_id, provider, provider_transaction_id, amount, currency, db):
        amount = float(amount)
        user_uuid = User.get_by_id(user_id, scope='all')['uuid']

        from paypalrestsdk import Payment, ResourceNotFound

        try:
            payment = Payment.find(provider_transaction_id)
            logger.info(payment)

            # amount
            provider_amount = float(payment['transactions'][0]['amount']['total'])
            provider_currency = payment['transactions'][0]['amount']['currency']
            logger.info(str(provider_amount) + ' ' + str(provider_currency))

            # fee
            try:
                fee = payment['transactions'][0]['related_resources'][0]['sale']['transaction_fee']
                logger.info(fee)
                provider_fee_amount = float(fee['value'])
                provider_fee_currency = fee['currency']
                logger.info(str(provider_fee_amount) + ' ' + str(provider_fee_currency))
            except:
                logger.info('No data about fee')
                provider_fee_amount = 0
                provider_fee_currency = provider_currency

            if amount != provider_amount:
                # fraud
                logger.info('Amounts do not match')
                raise NotAcceptableException()

            if currency.lower() != provider_currency.lower():
                # fraud
                logger.info('Currencies do not match')
                raise NotAcceptableException()

            if currency.lower() != provider_fee_currency.lower():
                # do not know how to handle it
                logger.info('Fee currencies do not match')
                raise NotAcceptableException()

            # subtract fee
            amount -= provider_fee_amount
            logger.info('Amount - fee = ' + str(provider_amount))

            if amount < 0:
                # fee > amount
                raise NotAcceptableException()

        except ResourceNotFound as error:
            logger.warn(error)
            raise ResourceIsNotFound()

        # write to db
        with db.t():
            # transaction
            transaction_id = Transaction.add_deposit_db(
                db,
                user_id, user_uuid,
                amount, provider_fee_amount, currency,
                'paypal', provider_transaction_id,
            )
            if not transaction_id:
                raise ConflictException()

            # increase balance
            UserAccount.update_user_balance(db, user_id, +amount, currency)

        # update statistics sync.
        # TODO: make it async.
        from models.statistics import Statistics
        Statistics.update_statistics_via_transaction(user_id, transaction_id)

        #
        return transaction_id



