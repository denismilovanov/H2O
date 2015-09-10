from decorators import *

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class UserDevice:
    @staticmethod
    @raw_queries()
    def delete_push_token(user_id, push_token, db):
        logger.info('delete_push_token')
        logger.info(push_token)

        db.select_field('''
            SELECT main.delete_user_push_token(%(user_id)s, %(push_token)s);
        ''', user_id=user_id, push_token=push_token)





