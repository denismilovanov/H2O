from decorators import *

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class UserSession:
    @staticmethod
    @raw_queries()
    def upsert_user_session(user_id, device_type, push_token, db):
        logger.info('upsert_user_session')

        from H2O.settings import ACCESS_TOKEN_EXPIRES_IN, REFRESH_TOKEN_EXPIRES_IN

        session = db.select_record('''
            SELECT  t.*,
                    public.format_datetime(now() + interval '1 second' * %(atei)s) AS access_token_expires_at,
                    public.format_datetime(now() + interval '1 second' * %(rtei)s) AS refresh_token_expires_at
                FROM main.upsert_user_session(%(user_id)s, %(device_type)s, %(push_token)s)
                AS t(id bigint, access_token varchar, refresh_token varchar);
        ''',
            user_id=user_id, device_type=device_type, push_token=push_token,
            atei=ACCESS_TOKEN_EXPIRES_IN, rtei=REFRESH_TOKEN_EXPIRES_IN
        )

        return {
            'access_token': session['access_token'],
            'refresh_token': session['refresh_token'],
            'access_token_expires_in': ACCESS_TOKEN_EXPIRES_IN,
            'refresh_token_expires_in': REFRESH_TOKEN_EXPIRES_IN,
            'access_token_expires_at': session['access_token_expires_at'],
            'refresh_token_expires_at': session['refresh_token_expires_at'],
        }

    @staticmethod
    @raw_queries()
    def get_user_uuid_by_access_token(access_token, db):
        logger.info('get_user_uuid_by_access_token')

        uuid = db.select_field('''
            SELECT main.get_user_uuid_by_access_token(%(access_token)s);
        ''', access_token=access_token)
        logger.info(uuid)

        return uuid

    @staticmethod
    @raw_queries()
    def refresh_access_token(refresh_token, db):
        logger.info('refresh_access_token')

        from H2O.settings import ACCESS_TOKEN_EXPIRES_IN

        data = db.select_record('''
            SELECT  main.refresh_access_token(%(refresh_token)s) AS access_token,
                    public.format_datetime(now() + interval '1 second' * %(atei)s) AS access_token_expires_at
        ''', refresh_token=refresh_token, atei=ACCESS_TOKEN_EXPIRES_IN)

        return data['access_token'], data['access_token_expires_at']

    @staticmethod
    @raw_queries()
    def drop_access_tokens(db):
        from H2O.settings import ACCESS_TOKEN_EXPIRES_IN, REFRESH_TOKEN_EXPIRES_IN
        db.select_field('''
            SELECT main.drop_access_tokens(%(ACCESS_TOKEN_EXPIRES_IN)s);
        ''', ACCESS_TOKEN_EXPIRES_IN=ACCESS_TOKEN_EXPIRES_IN)

    @staticmethod
    @raw_queries()
    def drop_refresh_tokens(db):
        from H2O.settings import ACCESS_TOKEN_EXPIRES_IN, REFRESH_TOKEN_EXPIRES_IN
        db.select_field('''
            SELECT main.drop_refresh_tokens(%(REFRESH_TOKEN_EXPIRES_IN)s);
        ''', REFRESH_TOKEN_EXPIRES_IN=REFRESH_TOKEN_EXPIRES_IN)

    @staticmethod
    @raw_queries()
    def delete_session(user_id, access_token, db):
        db.select_field('''
            SELECT main.drop_all_tokens_by_access_token(%(access_token)s);
        ''', access_token=access_token)




