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
            from H2O.settings import FACEBOOK_TIMEOUT
            graph = facebook.GraphAPI(access_token=access_token, version="2.4", timeout=FACEBOOK_TIMEOUT)

            #
            profile = graph.get_object('me')

            # avatar
            avatar = graph.get_object(profile['id'] + '/picture?type=square&width=100&height=100')
            avatar_url = avatar.get('url')

        except Exception, e:
            logger.warn(e)
            # ok, let's raise
            raise FacebookException(e)

        return {
            'name': profile['name'],
            'avatar_url': avatar_url,
            'id': profile['id'],
        }

    @staticmethod
    def get_user_friends_ids(access_token, facebook_id):
        try:
            from H2O.settings import FACEBOOK_TIMEOUT
            graph = facebook.GraphAPI(access_token=access_token, version="2.4", timeout=FACEBOOK_TIMEOUT)

            facebook_friends_ids = []
            friends_url = str(facebook_id) + '/friends'

            while True:
                logger.info(friends_url)
                facebook_friends = graph.get_object(friends_url)

                try:
                    friends_batch = facebook_friends['data']
                    for friend in friends_batch:
                        facebook_friends_ids.append(int(friend['id']))

                    friends_url = facebook_friends['paging']['next']
                except Exception, e:
                    break

                if not friends_batch:
                    break

            return facebook_friends_ids

        except Exception, e:
            logger.warn(e)
            return False
