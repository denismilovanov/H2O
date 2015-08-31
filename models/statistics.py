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
            SELECT transaction_direction, users_ids, transactions_count, users_count
                FROM statistics.get_statistics_overall(%(user_id)s);
        ''', user_id=user_id)

        result = {}

        for record in statistics:
            transaction_direction = str(record['transaction_direction']) + 's'
            result[transaction_direction] = {
                'transactions_count': record['transactions_count'],
                'users_count': record['users_count'],
                'users': User.get_all_by_ids(record['users_ids'], scope='public_profile')
            }

        return result

    @staticmethod
    @raw_queries()
    def get_statistics_counter_users(user_id, transaction_direction, limit, count, db):
        users_ids = []

        return User.get_all_by_ids(users_ids, scope='public_profile')

    @staticmethod
    @raw_queries()
    def create_user_records(user_id, db):
        db.select_field('''
            SELECT statistics.create_user_records(%(user_id)s);
        ''', user_id=user_id)

        return True

