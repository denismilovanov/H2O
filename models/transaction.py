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
    def get_transactions_raw(users_ids, from_date, to_date, direction, db):
        return db.select_table('''
            SELECT ''' + Transaction.scope('public') + ''', date(created_at) AS date, counter_user_id, user_id
                FROM main.get_transactions_by_users_ids_and_dates(%(users_ids)s, %(from_date)s::date, %(to_date)s::date, %(direction)s);
        ''', users_ids=users_ids, from_date=from_date, to_date=to_date, direction=direction)

    @staticmethod
    def extract_counter_users_ids(transactions):
        # counter users ids
        counter_users_ids = []
        for transaction in transactions:
            counter_users_ids.append(transaction['counter_user_id'])

        return counter_users_ids

    @staticmethod
    def extract_users_ids(transactions):
        # users ids
        users_ids = []
        for transaction in transactions:
            users_ids.append(transaction['user_id'])

        return users_ids

    @staticmethod
    def split_transactions_by_dates(transactions):
        result = {}

        for transaction in transactions:
            date = str(transaction['date'])

            del transaction['counter_user_id']
            del transaction['user_id']
            del transaction['date']

            try:
                result[date].append(transaction)
            except Exception, e:
                result[date] = []
                result[date].append(transaction)

        return result

    @staticmethod
    @raw_queries()
    def get_transactions(user_id, whose, direction, from_date, to_date, db):
        if whose == 'my':
            # all transactions of me
            users_ids = [user_id]
        elif whose == 'follows':
            # my follows
            users_ids = follows_ids = UserFollow.get_user_follows_ids(user_id)

        # all transactions of them
        transactions = Transaction.get_transactions_raw(users_ids, from_date, to_date, direction, db)

        # extract counter users ids
        counter_users_ids = Transaction.extract_counter_users_ids(transactions)

        # get them all
        counter_users = User.get_all_by_ids(counter_users_ids, scope='public_profile')

        # gather all
        result = {
            'transactions_by_dates': Transaction.split_transactions_by_dates(transactions),
            'users': counter_users,
        }

        if whose == 'follows':
            result['follows'] = User.get_all_by_ids(follows_ids, scope='public_profile')

        # we are ready!
        return result


