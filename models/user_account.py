from decorators import *

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class UserAccount:
    @staticmethod
    @raw_queries()
    def get_user_account(user_id, db):
        account = db.select_record('''
            SELECT * FROM billing.get_user_account(%(user_id)s);
        ''', user_id=user_id)

        return account

    @staticmethod
    def create_user_accounts(user_id, db):
        db.select_field('''
            SELECT billing.create_user_accounts(%(user_id)s);
        ''', user_id=user_id)

        return True

    @staticmethod
    def update_user_balance(db, user_id, amount, currency, hold=None):
        return db.select_field('''
            SELECT billing.update_user_balance(%(user_id)s, %(amount)s, %(hold)s, %(currency)s);
        ''', user_id=user_id, amount=amount, currency=currency, hold=hold)
