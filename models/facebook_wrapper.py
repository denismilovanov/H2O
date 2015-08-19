import facebook
from exceptions import FacebookException

class FacebookWrapper:
    @staticmethod
    def get_user_data(access_token):
        try:
            graph = facebook.GraphAPI(access_token=access_token)
            profile = graph.get_object("me")
        except Exception, e:
            # ok, let's raise
            raise FacebookException(e)

        return {
            'first_name': profile['first_name'],
            'last_name': profile['last_name'],
        }
