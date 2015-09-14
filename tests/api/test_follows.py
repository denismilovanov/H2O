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

        follows_controller = self.follows_controller + '/10000000-0000-0000-0000-000000000000'
        response = self.client.post(follows_controller, {}, format=self.format, headers=headers)
        self.assertTrue(response.status_code == status.HTTP_404_NOT_FOUND)

        # get my

        follows = self.get_follows('my', None, headers)

        # first of them

        follow = self.get_profile(follows[0]['uuid'], headers)

        # search him by name

        follows = self.get_follows('my', follow['name'], headers)
        self.assertTrue(len(follows) > 0)

        # get others

        follows = self.get_follows('00000002-0000-0000-0000-000000000002', None, headers)

        # delete

        follows_controller = self.follows_controller + '/00000009-0000-0000-0000-000000000009'
        response = self.client.delete(follows_controller, {}, format=self.format, headers=headers)
        self.assertTrue(response.status_code == status.HTTP_204_NO_CONTENT)

        # delete again

        follows_controller = self.follows_controller + '/00000009-0000-0000-0000-000000000009'
        response = self.client.delete(follows_controller, {}, format=self.format, headers=headers)
        self.assertTrue(response.status_code == status.HTTP_404_NOT_FOUND)


