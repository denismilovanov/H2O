from decorators import *

import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class UserSession:
    @staticmethod
    @raw_queries()
    def upsert_user_session(user_id, device_id, device_type, push_token, db):
        logger.debug('upsert_user_session')

        session = db.select_record('''
            SELECT *
                FROM main.upsert_user_session(%(user_id)s, %(device_id)s, %(device_type)s, %(push_token)s)
                AS t(id bigint, access_token varchar, refresh_token varchar);
        ''', user_id=user_id, device_id=device_id, device_type=device_type, push_token=push_token)

        from H2O.settings import ACCESS_TOKEN_EXPIRES_IN, REFRESH_TOKEN_EXPIRES_IN
        return {
            'access_token': session['access_token'],
            'refresh_token': session['refresh_token'],
            'access_token_expires_in': ACCESS_TOKEN_EXPIRES_IN,
            'refresh_token_expires_in': REFRESH_TOKEN_EXPIRES_IN,
        }



