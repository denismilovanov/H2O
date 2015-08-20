from django.conf import settings
from tests.api.test_case import MyAPITestCase
from models import *
from rest_framework import status
import json

class ProfileTestCase(MyAPITestCase):
    def test1(self):
        data = {
            'status': 'i_have_less_than_enough_money',
            'visibility': 'visible_for_friends',
        }
        headers = self.authorization()['headers']

        response = self.client.patch(self.profile_controller, data, format=self.format, headers=headers)
        self.assertTrue(response.status_code == status.HTTP_204_NO_CONTENT)



