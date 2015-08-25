import facebook
from exceptions import FacebookException

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class FacebookWrapper:
    @staticmethod
    def get_user_data(access_token):
        logger.info(access_token)

        # test cases will pass here special access token:
        import re
        m = re.search('TEST_TOKEN_(\d+)', access_token)
        if m:
            test_user_id = m.group(1)
            return {
                'name': 'Test ' + str(test_user_id),
                'avatar_url': None,
                'id': -1 * int(test_user_id), # tests users have negative ids
            }

        # normal access token
        try:
            graph = facebook.GraphAPI(access_token=access_token, version="2.4")
            logger.info(graph)

            profile = graph.get_object('me')
            logger.info(profile)

            avatar = graph.get_object(profile['id'] + '/picture?type=large')
            avatar_url = None

            try:
                avatar_url = avatar['url']
            except Exception, e:
                pass

        except Exception, e:
            logger.info(e)
            # ok, let's raise
            raise FacebookException(e)

        return {
            'name': profile['name'],
            'avatar_url': avatar_url,
            'id': profile['id'],
        }
