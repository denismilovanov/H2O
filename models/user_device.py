from decorators import *

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class UserDevice:
    @staticmethod
    @raw_queries()
    def upsert_push_token(user_id, push_token, db):
        logger.info('upsert_push_token')
        logger.info(push_token)

        device_type = None

        if 0 < len(push_token) < 100:
            device_type = 'ios'
        if len(push_token) > 100:
            device_type = 'android'

        if device_type:
            db.select_field('''
                SELECT main.upsert_user_push_token(%(user_id)s, %(device_type)s, %(push_token)s);
            ''', user_id=user_id, push_token=push_token, device_type=device_type)

    @staticmethod
    @raw_queries()
    def delete_push_token(user_id, push_token, db):
        logger.info('delete_push_token')
        logger.info(push_token)

        db.select_field('''
            SELECT main.delete_user_push_token(%(user_id)s, %(push_token)s);
        ''', user_id=user_id, push_token=push_token)

    @staticmethod
    @raw_queries()
    def drop_push_tokens(db):
        from H2O.settings import IOS_PUSH_TOKEN_EXPIRES_IN, ANDROID_PUSH_TOKEN_EXPIRES_IN
        db.select_field('''
            SELECT main.drop_push_tokens(%(IOS_PUSH_TOKEN_EXPIRES_IN)s, %(ANDROID_PUSH_TOKEN_EXPIRES_IN)s);
        ''', IOS_PUSH_TOKEN_EXPIRES_IN=IOS_PUSH_TOKEN_EXPIRES_IN, ANDROID_PUSH_TOKEN_EXPIRES_IN=ANDROID_PUSH_TOKEN_EXPIRES_IN)




