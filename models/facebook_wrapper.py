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
            avatar = graph.get_object(profile['id'] + '/picture?type=large')
            avatar_url = None
            try:
                avatar_url = avatar['url']
            except Exception, e:
                pass

            facebook_friends_ids = []

            # am I new user?
            from models.user_network import UserNetwork
            me_id = UserNetwork.find_user_by_network(1, profile['id'])

            # yes, I am
            if not me_id:
                # friends
                facebook_friends_ids = FacebookWrapper.get_user_friends_ids(graph, profile['id'])

        except Exception, e:
            logger.info(e)
            # ok, let's raise
            raise FacebookException(e)

        return {
            'name': profile['name'],
            'avatar_url': avatar_url,
            'id': profile['id'],
            'facebook_friends_ids': facebook_friends_ids,
        }

    @staticmethod
    def get_user_friends_ids(graph, id):
        facebook_friends_ids = []
        friends_url = id + '/friends'

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
