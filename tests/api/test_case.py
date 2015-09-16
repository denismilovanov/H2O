from rest_framework.test import APITestCase
from rest_framework import status
import json
import requests
import re
import cookielib

class MyAPITestCase(APITestCase):
    multi_db = True

    def get_facebook_access_token(self):
        from H2O.settings import BASE_DIR, FACEBOOK_CLIENT_ID
        url = 'https://www.facebook.com/dialog/oauth?client_id=' + FACEBOOK_CLIENT_ID + '&redirect_uri=https://www.facebook.com/connect/login_success.html&scope=basic_info,email,public_profile,user_about_me,user_birthday,user_education_history,user_friends,user_likes,user_location,user_photos,user_relationship_details&response_type=token'
        jar = cookielib.LWPCookieJar(BASE_DIR + '/resources/tests/facebook_cookies.txt')
        jar.load()
        r = requests.get(url, cookies=jar)
        m = re.search('access_token=([A-Za-z\d]+)', r.url)
        access_token = m.group(1)
        return access_token

    def get_balance(self, headers):
        return self.get_profile('me', headers)['balance']

    def get_follows(self, who, search_query, headers):
        follows_controller = self.follows_controller + '/' + who
        if search_query:
            response = self.client.get(follows_controller, {
                'limit': 10,
                'offset': 0,
                'search_query': search_query,
            }, format=self.format, headers=headers)
        else:
            response = self.client.get(follows_controller, {
                'limit': 10,
                'offset': 0,
            }, format=self.format, headers=headers)
        self.assertTrue(response.status_code == status.HTTP_200_OK)
        return json.loads(response.content)

    def get_profile(self, who, headers):
        user_controller = self.user_controller + who
        response = self.client.get(user_controller, {}, format=self.format, headers=headers)
        self.assertTrue(response.status_code == status.HTTP_200_OK)
        profile = json.loads(response.content)
        return profile

    def authorization(self, user_id=1, facebook_token=None):
        data = {
            'network_id': 1,
            'access_token': facebook_token if facebook_token else 'TEST_TOKEN_' + str(user_id),
            'invite_code': 'Q123',
            'device_type': 'ios',
            'push_token': '1' * 64,
        }

        response = self.client.post(self.session_controller, data, format=self.format)
        self.assertTrue(response.status_code == status.HTTP_201_CREATED)

        session = json.loads(response.content)

        return {
            'headers': {
                'Access-Token': session['session']['access_token'],
            },
            'session': session,
        }

    session_controller = '/v1/session'
    profile_controller = '/v1/profile'
    user_controller = '/v1/users/'
    invite_codes_controller = '/v1/invite_codes'
    follows_controller = '/v1/follows'
    supports_controller = '/v1/supports'
    receives_controller = '/v1/receives'
    transactions_controller = '/v1/transactions'
    deposits_controller = '/v1/deposits'
    withdrawals_controller = '/v1/withdrawals'
    statistics_controller = '/v1/statistics'
    notifications_controller = '/v1/notifications'
    graph_controller = '/v1/graph'
    error_controller = '/v1/error'
    format = 'json'


