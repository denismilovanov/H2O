from decorators import *

import logging
logging.basicConfig(level=logging.INFO)
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

    @staticmethod
    @raw_queries()
    def upsert_network(user_uuid, network_id, network_user_id, access_token, db):
        logger.info('upsert_network')

        return db.select_field('''
            SELECT main.upsert_user_network(%(user_uuid)s, %(network_id)s, %(network_user_id)s, %(access_token)s);
        ''', user_uuid=user_uuid, network_id=network_id, network_user_id=network_user_id, access_token=access_token)

