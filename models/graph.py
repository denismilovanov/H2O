from decorators import *

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Graph:
    @staticmethod
    @raw_queries(['auth'])
    def get_last_num_in_generation(generation, auth):
        logger.info('get_last_num_in_generation')

        last_num_in_generation = auth.select_field('''
            SELECT main.get_last_num_in_generation(%(generation)s);
        ''', generation=generation)

        return last_num_in_generation
