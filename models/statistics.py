from decorators import *
from models import User, UserFollow

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Statistics:
    @staticmethod
    @raw_queries()
    def get_statistics_overall(user_id, db):
        statistics = db.select_table('''
            SELECT transaction_direction, transactions_count, users_count
                FROM statistics.get_statistics_overall(%(user_id)s);
        ''', user_id=user_id)

        result = {}

        for record in statistics:
            result[str(record['transaction_direction']) + 's'] = {
                'transactions_count': record['transactions_count'],
                'users_count': record['users_count'],
                'users': Statistics.get_statistics_counter_users_inner(user_id, record['transaction_direction'], 5, 0, db)
            }

        return result

    @staticmethod
    @raw_queries()
    def get_statistics_counter_users(user_id, transaction_direction, limit, offset, db):
        return Statistics.get_statistics_counter_users_inner(user_id, transaction_direction, limit, offset, db)

    @staticmethod
    def get_statistics_counter_users_inner(user_id, transaction_direction, limit, offset, db):
        # get stat
        statistics = db.select_table('''
            SELECT *
                FROM statistics.get_statistics_counter_users(%(user_id)s, %(transaction_direction)s, %(limit)s, %(offset)s);
        ''', user_id=user_id, transaction_direction=transaction_direction, limit=limit, offset=offset)

        # build hash from transactons_count
        transactions_counts = dict([(record['counter_user_id'], record['transactions_count']) for record in statistics])

        # collect users ids
        users_ids = [record['counter_user_id'] for record in statistics]

        # get all users
        users = User.get_all_by_ids(users_ids, scope='public_profile_with_id')

        # add transactions_count to user
        for user in users:
            user['transactions_count'] = transactions_counts[user['id']]
            del user['id']

        #
        return users

    @staticmethod
    @raw_queries()
    def create_user_records(user_id, db):
        db.select_field('''
            SELECT statistics.create_user_records(%(user_id)s);
        ''', user_id=user_id)

        return True

