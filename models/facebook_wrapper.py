import facebook
from exceptions import FacebookException

import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class FacebookWrapper:
    @staticmethod
    def get_user_data(access_token):
        logger.debug(access_token)
        try:
            graph = facebook.GraphAPI(access_token=access_token)
            logger.debug(graph)
            profile = graph.get_object("me")
            logger.debug(profile)
        except Exception, e:
            # ok, let's raise
            raise FacebookException(e)

        return {
            'first_name': profile['first_name'],
            'last_name': profile['last_name'],
        }
