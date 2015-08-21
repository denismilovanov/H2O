from django.conf import settings
from tests.api.test_case import MyAPITestCase
from models import *
from rest_framework import status
import json

class SessionTestCase(MyAPITestCase):
    def test1(self):
        authorization = self.authorization()
        headers = authorization['headers']
        session = authorization['session']

        # get self

        user_controller = self.user_controller + session['user']['user_uuid']
        headers = {
            'Access-Token': session['session']['access_token']
        }
        response = self.client.get(user_controller, {}, format=self.format, headers=headers)
        self.assertTrue(response.status_code == status.HTTP_200_OK)

        # my codes

        controller = self.invite_codes_controller
        response = self.client.get(controller, {}, format=self.format, headers=headers)
        self.assertTrue(response.status_code == status.HTTP_200_OK)

        # all

        controller = self.user_controller
        response = self.client.get(controller, {}, format=self.format, headers=headers)
        self.assertTrue(response.status_code == status.HTTP_200_OK)

        # not found

        user_controller = self.user_controller + '00000000-0000-0000-0000-000000000000'
        response = self.client.get(user_controller, {}, format=self.format, headers=headers)
        self.assertTrue(response.status_code == status.HTTP_404_NOT_FOUND)

        # unauthorized

        headers['Access-Token'] = 'wrong'
        response = self.client.get(user_controller, {}, format=self.format, headers=headers)
        self.assertTrue(response.status_code == status.HTTP_401_UNAUTHORIZED)

        # refresh

        response = self.client.patch(self.session_controller, {
            'refresh_token': session['session']['refresh_token']
        }, format=self.format)
        self.assertTrue(response.status_code == status.HTTP_200_OK)


