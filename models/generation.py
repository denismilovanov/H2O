from decorators import *
from models.user import User
from models.user_follow import UserFollow


import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Generation:
    @staticmethod
    @raw_queries()
    def get_last_num_in_generation(generation, db):
        logger.info('get_last_num_in_generation')

        last_num_in_generation = db.select_field('''
            SELECT main.get_last_num_in_generation(%(generation)s);
        ''', generation=generation)

        return last_num_in_generation

    @staticmethod
    @raw_queries()
    def get_users_counts(db):
        generations = db.select_table('''
            SELECT * FROM main.get_generations();
        ''')

        result = []
        for generation in generations:
            if generation['users_count'] == 0:
                break
            result.append(generation['users_count'])

        return result

    @staticmethod
    @raw_queries()
    def get_zero_generation(db):
        first_generation_users = db.select_table('''
            SELECT main.get_users_ids_by_generation(0) AS user_id;
        ''')

        first_generation_users_ids = [first_generation_user['user_id'] for first_generation_user in first_generation_users]

        return User.get_all_by_ids(first_generation_users_ids, scope='graph')

    @staticmethod
    @raw_queries()
    def get_follows(user_id, db):
        users_follows_ids = UserFollow.get_user_follows_ids(user_id)

        return User.get_all_by_ids(users_follows_ids, scope='graph')

    @staticmethod
    @raw_queries()
    def get_followed_by(user_id, db):
        users_followed_by_ids = UserFollow.get_user_followed_by_ids(user_id)

        return User.get_all_by_ids(users_followed_by_ids, scope='graph')
