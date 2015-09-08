from decorators import *
from models import User, UserFollow

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Transaction:
    @staticmethod
    def scope(scope):
        if scope == 'public':
            return ', '.join(['amount', 'currency', 'status', 'direction', 'user_uuid', 'counter_user_uuid'])
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
    def get_transactions_by_offset_raw(users_ids, limit, offset, db):
        return db.select_table('''
            SELECT ''' + Transaction.scope('public') + ''',
                    public.format_datetime(created_at) AS created_at,
                    counter_user_id, user_id
                FROM billing.get_transactions_by_users_ids_and_offset(%(users_ids)s, %(limit)s, %(offset)s);
        ''', users_ids=users_ids, limit=limit, offset=offset)

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
    def extract_counter_users_ids(transactions):
        # counter users ids
        counter_users_ids = []
        for transaction in transactions:
            counter_users_ids.append(transaction['counter_user_id'])

        return list(set(counter_users_ids))

    @staticmethod
    def extract_users_ids(transactions):
        # users ids
        users_ids = []
        for transaction in transactions:
            users_ids.append(transaction['user_id'])

        return list(set(users_ids))

    @staticmethod
    def get_users_and_follows_ids(whose, user_id):
        if whose == 'my':
            # all transactions of me
            users_ids = [user_id]
            follows_ids = []
        elif whose == 'follows':
            # my follows
            users_ids = follows_ids = UserFollow.get_user_follows_ids(user_id)

        return users_ids, follows_ids

    @staticmethod
    @raw_queries()
    def get_transactions_by_dates(user_id, whose, direction, from_date, to_date, db):
        #
        users_ids, follows_ids = Transaction.get_users_and_follows_ids(whose, user_id)

        # all transactions of them
        transactions = Transaction.get_transactions_by_dates_raw(users_ids, from_date, to_date, direction, db)

        #
        return Transaction.prepare_transactions_response(transactions, whose, follows_ids)


    @staticmethod
    @raw_queries()
    def get_transactions_by_offset(user_id, whose, limit, offset, db):
        #
        users_ids, follows_ids = Transaction.get_users_and_follows_ids(whose, user_id)

        # all transactions of them
        transactions = Transaction.get_transactions_by_offset_raw(users_ids, limit, offset, db)

        #
        return Transaction.prepare_transactions_response(transactions, whose, follows_ids)


    @staticmethod
    def prepare_transactions_response(transactions, whose, follows_ids):
        # extract counter users ids
        counter_users_ids = Transaction.extract_counter_users_ids(transactions)

        # append follows to counters
        if whose == 'follows':
            counter_users_ids = counter_users_ids + follows_ids

        # get them all
        counter_users = User.get_all_by_ids(counter_users_ids, scope='public_profile')

        # remove some indeces
        for transaction in transactions:
            del transaction['counter_user_id']
            del transaction['user_id']

        # gather all
        result = {
            'transactions': transactions,
            'users': counter_users,
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
                %(direction)s, %(amount)s, %(currency)s, %(is_anonymous)s
            );
        ''',
            user_id=user_id, user_uuid=user_uuid,
            counter_user_id=counter_user_id, counter_user_uuid=counter_user_uuid,
            direction=direction,
            amount=amount, currency=currency, is_anonymous=is_anonymous
        )

    @staticmethod
    def update_user_balance(db, user_id, amount, currency):
        db.select_field('''
            SELECT billing.update_user_balance(%(user_id)s, %(amount)s, %(currency)s);
        ''', user_id=user_id, amount=amount, currency=currency)

    @staticmethod
    @raw_queries()
    def add_support(user_id, counter_user_id, amount, currency, is_anonymous, db):
        amount = float(amount)
        user_uuid = User.get_all_by_ids([user_id], scope='all')[0]['uuid']
        counter_user_uuid = User.get_all_by_ids([counter_user_id], scope='all')[0]['uuid']

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
                Transaction.update_user_balance(db, user_id, amount * -1, currency)

                # receive
                counter_transaction_id = Transaction.add_transaction_raw(
                    db,
                    counter_user_id, counter_user_uuid,
                    user_id, user_uuid,
                    'receive',
                    amount, currency, is_anonymous
                )

                # increase balance
                Transaction.update_user_balance(db, counter_user_id, amount, currency)

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
    def add_deposit(user_id, amount, currency, db):
        amount = float(amount)
        user_uuid = User.get_all_by_ids([user_id], scope='all')[0]['uuid']

        transaction_id = Transaction.add_transaction_raw(
            db,
            user_id, user_uuid,
            None, None,
            amount, currency, False
        )

        return transaction_id
