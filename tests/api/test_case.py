from rest_framework.test import APITestCase
from rest_framework import status
import json


class MyAPITestCase(APITestCase):
    multi_db = True

    def authorization(self, user_id=1, facebook_token=None):
        data = {
            'network_id': 1,
            'access_token': facebook_token if facebook_token else 'TEST_TOKEN_' + str(user_id),
            'invite_code': 'Q123',
            'device_type': 'ios',
            'push_token': 'push',
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
    statistics_controller = '/v1/statistics'
    notifications_controller = '/v1/notifications'
    format = 'json'


