from django.conf import settings
from tests.api.test_case import MyAPITestCase
from models import *
from rest_framework import status
import json

class FollowsTestCase(MyAPITestCase):
    def test1(self):
        authorization = self.authorization()
        headers = authorization['headers']
        session = authorization['session']

        # follows

        follows_controller = self.follows_controller + '/00000009-0000-0000-0000-000000000009'
        response = self.client.post(follows_controller, {}, format=self.format, headers=headers)
        self.assertTrue(response.status_code == status.HTTP_201_CREATED)

        # follows again

        response = self.client.post(follows_controller, {}, format=self.format, headers=headers)
        self.assertTrue(response.status_code == status.HTTP_406_NOT_ACCEPTABLE)

        # not found

        follows_controller = self.follows_controller + '/00000000-0000-0000-0000-000000000000'
        response = self.client.post(follows_controller, {}, format=self.format, headers=headers)
        self.assertTrue(response.status_code == status.HTTP_404_NOT_FOUND)

        # get my

        follows_controller = self.follows_controller + '/my'
        response = self.client.get(follows_controller, {}, format=self.format, headers=headers)
        self.assertTrue(response.status_code == status.HTTP_200_OK)

        # get others

        follows_controller = self.follows_controller + '/00000002-0000-0000-0000-000000000002'
        response = self.client.get(follows_controller, {}, format=self.format, headers=headers)
        self.assertTrue(response.status_code == status.HTTP_200_OK)


