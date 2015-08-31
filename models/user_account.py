from decorators import *

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class UserAccount:
    @staticmethod
    @raw_queries()
    def get_user_account(user_id, db):
        account = db.select_record('''
            SELECT * FROM main.get_user_account(%(user_id)s);
        ''', user_id=user_id)

        return account

    @staticmethod
    @raw_queries()
    def create_user_accounts(user_id, db):
        db.select_field('''
            SELECT main.create_user_accounts(%(user_id)s);
        ''', user_id=user_id)

        return True
