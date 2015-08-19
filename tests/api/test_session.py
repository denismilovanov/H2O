from django.conf import settings
from rest_framework.test import APITestCase
from models import *
from rest_framework import status
import json

class SessionTestCase(APITestCase):
    def test1(self):
        session_controller = '/v1/session'
        method = self.client.post
        format = 'json'

        data = {
            'credentials': {
                'network_id': 1,
                'access_token': 'CAAGm0PX4ZCpsBAOi6acVijldkNXHSTzLikTdrKGp5uMzpTDXmZAR5vKHZCLyAQ1biZAGya68y6d2qExuhaGJZCnEfvigNs3OqIkzglULlhNkoGSI7d7SLfgTnQBH1BLGhekA2G9SKiE6AVFOXZCMzj3l7nWlYaFEeVNJGTuZAKYZAZCH0GGT9zKMP2wjEYP1f0LiAzeZAVdSjpSAZDZD',
                'user_id': 10153386713348088,
            },
            'invite_code': 'Q123',
        }

        response = method(session_controller, data, format=format)
        print response.content
        print response.status_code
        self.assertTrue(response.status_code == status.HTTP_201_CREATED)

        response = method(session_controller, data, format=format)
        self.assertTrue(response.status_code == status.HTTP_201_CREATED)

        session = json.loads(response.content)

        # get self

        user_controller = '/v1/user/' + session['user']['user_uuid']
        headers = {
            'Access-Token': session['session']['access_token']
        }
        user_method = self.client.get
        response = user_method(user_controller, {}, format=format, headers=headers)
        self.assertTrue(response.status_code == status.HTTP_200_OK)

        # not found

        user_controller = '/v1/user/00000000-0000-0000-0000-000000000000'
        response = user_method(user_controller, {}, format=format, headers=headers)
        self.assertTrue(response.status_code == status.HTTP_404_NOT_FOUND)

        # unauthorized

        headers['Access-Token'] = 'wrong'
        response = user_method(user_controller, {}, format=format, headers=headers)
        self.assertTrue(response.status_code == status.HTTP_401_UNAUTHORIZED)

        # refresh

        session_method = self.client.patch
        response = session_method(session_controller, {
            'refresh_token': session['session']['refresh_token']
        }, format=format)
        self.assertTrue(response.status_code == status.HTTP_200_OK)


