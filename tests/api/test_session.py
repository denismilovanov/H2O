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
                'access_token': 'CAAGm0PX4ZCpsBAGtJjRCfiQC3b58ple8ASu5jJG75ghGYUCpgjzYY71skT0UlLOi6dUWvqX6Vddcn1Pk4Ur2ncvEG3OtkqTAEndvGi2febjJAZAEImIbGiGtpPZBfv0SDIk2Q9c5c7x1TOCESLj2ifhIgaiLLal2ffpkUKOu6g1qx7FQ13uQagUW2MkmQI3NGOSa8yh7AZDZD',
                'user_id': 10153386713348088,
            },
            'invite_code': 'Q123',
        }

        response = method(session_controller, data, format=format)
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


