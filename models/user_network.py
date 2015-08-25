from decorators import *

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class UserNetwork:
    @staticmethod
    @raw_queries(['auth'])
    def get_new_user_id(auth):
        logger.info('get_new_user_id')
        user = auth.select_record('''
            SELECT * FROM main.get_new_user_id() AS t(user_id integer, user_uuid uuid);
        ''')
        logger.info(user)

        return user['user_id'], user['user_uuid']

    @staticmethod
    @raw_queries(['auth'])
    def find_user_by_network(network_id, user_network_id, auth):
        logger.info('find_user_by_network')
        logger.info(str(network_id) + ' ' + str(user_network_id))

        user_id = auth.select_field('''
            SELECT main.find_user_by_network(%(network_id)s, %(user_network_id)s);
        ''', network_id=network_id, user_network_id=user_network_id)
        logger.info(user_id)

        return user_id

    @staticmethod
    @raw_queries(['auth'])
    def get_user_networks(user_id, auth):
        facebook = auth.select_record('''
            SELECT * FROM main.get_user_networks(%(user_id)s);
        ''', user_id=user_id)

        return {
            'facebook': facebook
        }

    @staticmethod
    @raw_queries(['auth'])
    def upsert_network(user_uuid, network_id, network_user_id, access_token, auth):
        logger.info('upsert_network')

        return auth.select_field('''
            SELECT main.upsert_user_network(%(user_uuid)s, %(network_id)s, %(network_user_id)s, %(access_token)s);
        ''', user_uuid=user_uuid, network_id=network_id, network_user_id=network_user_id, access_token=access_token)

