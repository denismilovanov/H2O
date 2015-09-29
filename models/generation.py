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

