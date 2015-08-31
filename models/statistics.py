from decorators import *
from models import User, UserFollow

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Statistics:
    @staticmethod
    @raw_queries()
    def get_statistics_overall(user_id, db):
        statistics = db.select_record('''
            SELECT * FROM statistics.get_statistics_overall(%(user_id)s);
        ''', user_id=user_id)

        result = {
            'supports': {
                'transactions_count': statistics['supports_transactions_count'],
                'users_count': statistics['supports_users_count'],
                'users': User.get_all_by_ids(statistics['supports_users_ids'], scope='public_profile')
            },
            'receives': {
                'transactions_count': statistics['receives_transactions_count'],
                'users_count': statistics['receives_users_count'],
                'users': User.get_all_by_ids(statistics['receives_users_ids'], scope='public_profile')
            }
        }

        return result

    @staticmethod
    @raw_queries()
    def create_user_records(user_id, db):
        db.select_field('''
            SELECT statistics.create_user_records(%(user_id)s);
        ''', user_id=user_id)

        return True

