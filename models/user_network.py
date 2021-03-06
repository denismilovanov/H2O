from decorators import *

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class UserNetwork:
    @staticmethod
    @raw_queries()
    def get_new_user_id(db):
        logger.info('get_new_user_id')
        user = db.select_record('''
            SELECT * FROM main.get_new_user_id() AS t(user_id integer, user_uuid uuid);
        ''')
        logger.info(user)

        return user['user_id'], user['user_uuid']

    @staticmethod
    @raw_queries()
    def find_user_by_network(network_id, user_network_id, db):
        logger.info('find_user_by_network')
        logger.info(str(network_id) + ' ' + str(user_network_id))

        user_id = db.select_field('''
            SELECT main.find_user_by_network(%(network_id)s, %(user_network_id)s);
        ''', network_id=network_id, user_network_id=user_network_id)
        logger.info(user_id)

        return user_id

    @staticmethod
    @raw_queries()
    def find_users_by_network(network_id, users_network_ids, db):
        logger.info('find_users_by_network')
        logger.info(users_network_ids)

        users = db.select_table('''
            SELECT * FROM main.find_users_by_network(%(network_id)s, %(users_network_ids)s) AS user_id;
        ''', network_id=network_id, users_network_ids=users_network_ids)
        logger.info(users)

        return [user['user_id'] for user in users]

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

