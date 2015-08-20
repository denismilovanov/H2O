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
            graph = facebook.GraphAPI(access_token=access_token, version="2.4")
            logger.debug(graph)

            profile = graph.get_object('me')
            logger.debug(profile)

            avatar = graph.get_object(profile['id'] + '/picture?type=large')
            avatar_url = None

            try:
                avatar_url = avatar['url']
            except Exception, e:
                pass

        except Exception, e:
            logger.debug(e)
            # ok, let's raise
            raise FacebookException(e)

        return {
            'name': profile['name'],
            'avatar_url': avatar_url,
            'id': profile['id'],
        }
