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

        invite_codes = json.loads(response.content)

        invite_code = second_invite_code = None

        for code in invite_codes:
            if code['status'] == 'free':
                invite_code = code
            if code['status'] == 'free' and invite_code:
                second_invite_code = invite_codes[1]

        real_email = 'TEST_EMAIL_me@denismilovanov.net'

        # update

        controller = self.invite_codes_controller + '/' + invite_code['invite_code']

        response = self.client.patch(controller, {
            'email': 'me',
        }, format=self.format, headers=headers)
        self.assertTrue(response.status_code == status.HTTP_400_BAD_REQUEST)

        # update again

        controller = self.invite_codes_controller + '/' + invite_code['invite_code']

        response = self.client.patch(controller, {
            'email': real_email,
            'entrance_gift': False,
        }, format=self.format, headers=headers)
        self.assertTrue(response.status_code == status.HTTP_200_OK)

        # get again

        controller = self.invite_codes_controller + '/'
        response = self.client.get(controller, {}, format=self.format, headers=headers)
        self.assertTrue(response.status_code == status.HTTP_200_OK)

        # update again

        controller = self.invite_codes_controller + '/' + second_invite_code['invite_code']

        response = self.client.patch(controller, {
            'email': real_email,
        }, format=self.format, headers=headers)
        self.assertTrue(response.status_code == status.HTTP_406_NOT_ACCEPTABLE)

