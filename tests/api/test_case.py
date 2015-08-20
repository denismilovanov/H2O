from rest_framework.test import APITestCase
from rest_framework import status
import json


class MyAPITestCase(APITestCase):
    def authorization(self):
        data = {
            'network_id': 1,
            'access_token': 'CAAFs4iZCHulQBAP1qjTQISAFW60aA8MZBtZBWxUi5gGR5LZBZAZAftPwzZBaQXZChgbEAMByI7eAySOuLVm8piCV9sVetT94v2cqVkpFoaaSzjc6HqxByBW1DozJYeMhkuL0IumCEqKVeo1bJNxmTI4EBkHaDuZBZCLNERZAWoMlZAkXlQFbKTOMbh027jEHpjlOOfjZCzseskfkZAaSGUbFz61q3laeclW3P4Ujn8gpJS7AyqLQZDZD',
            'invite_code': 'Q123',
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
    user_controller = '/v1/user/'
    format = 'json'


