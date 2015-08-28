from decorators import *
from models import User, UserFollow

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Transaction:
    @staticmethod
    def scope(scope):
        if scope == 'public':
            return ', '.join(['amount', 'currency', 'status'])
        else:
            return '*'

    @staticmethod
    def get_transactions(users_ids, from_date, to_date, direction, db):
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
    @raw_queries()
    def get_my_supports(user_id, from_date, to_date, db):
        supports = Transaction.get_transactions([user_id], from_date, to_date, 'support', db)

        # extract counter users ids
        counter_users_ids = Transaction.extract_counter_users_ids(supports)

        # get them all
        counter_users = User.get_all_by_ids(counter_users_ids, scope='public_profile')

        # gather all
        result = {
            'transactions_by_dates': {},
            'counter_users': counter_users,
        }

        # split transactions by dates
        for support in supports:
            date = str(support['date'])

            del support['counter_user_id']
            del support['user_id']
            del support['date']

            try:
                result['transactions_by_dates'][date].append(support)
            except Exception, e:
                result['transactions_by_dates'][date] = []
                result['transactions_by_dates'][date].append(support)

        # we are ready!
        return result

    @staticmethod
    @raw_queries()
    def get_follows_supports(user_id, from_date, to_date, db):
        follows_ids =  UserFollow.get_user_follows_ids(user_id)

        # all transactions
        supports = Transaction.get_transactions(follows_ids, from_date, to_date, 'support', db)

        # extract counter users ids
        counter_users_ids = Transaction.extract_counter_users_ids(supports)

        # real follows who in transactions
        follows_ids = Transaction.extract_users_ids(supports)

        # get them all
        counter_users = User.get_all_by_ids(counter_users_ids, scope='public_profile')

        #
        follows = User.get_all_by_ids(follows_ids, scope='public_profile')

        # gather all
        result = {
            'transactions_by_dates': {},
            'follows': follows,
            'counter_users': counter_users,
        }

        # split transactions by dates
        for support in supports:
            date = str(support['date'])

            del support['counter_user_id']
            del support['user_id']
            del support['date']

            try:
                result['transactions_by_dates'][date].append(support)
            except Exception, e:
                result['transactions_by_dates'][date] = []
                result['transactions_by_dates'][date].append(support)

        # we are ready!
        return result


