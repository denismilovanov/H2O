from decorators import *

import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class UserNetwork:
    @staticmethod
    @raw_queries()
    def get_user_networks(user_id, db):
        facebook = db.select_record('''
            SELECT * FROM main.get_user_networks(%(user_id)s);
        ''', user_id=user_id)

        return {
            'facebook': facebook
        }
