from django.conf import settings
from tests.api.test_case import MyAPITestCase
from models import *
from rest_framework import status
import json

class InviteCodesTestCase(MyAPITestCase):
    def test1(self):
        session = self.authorization()

        headers = session['headers']

        controller = self.invite_codes_controller + '/'
        response = self.client.get(controller, {}, format=self.format, headers=headers)
        self.assertTrue(response.status_code == status.HTTP_200_OK)

        invite_codes = json.loads(response.content)['invite_codes']
        invite_code = invite_codes[0]

        # update

        controller = self.invite_codes_controller + '/' + invite_code['invite_code']

        response = self.client.patch(controller, {
            'email': 'me@denismilovanov.net',
        }, format=self.format, headers=headers)

        self.assertTrue(response.status_code == status.HTTP_204_NO_CONTENT)

        # get again

        controller = self.invite_codes_controller + '/'
        response = self.client.get(controller, {}, format=self.format, headers=headers)
        self.assertTrue(response.status_code == status.HTTP_200_OK)
