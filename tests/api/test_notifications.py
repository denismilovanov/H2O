from django.conf import settings
from tests.api.test_case import MyAPITestCase
from models import *
from rest_framework import status
import json

class NotificationsTestCase(MyAPITestCase):
    def test1(self):
        authorization = self.authorization()
        headers = authorization['headers']
        session = authorization['session']

        # my notifications

        response = self.client.get(self.notifications_controller, {
            'limit': '20',
            'offset': '0',
        }, format=self.format, headers=headers)
        self.assertTrue(response.status_code == status.HTTP_200_OK)

        notifications = json.loads(response.content)

        # delete notification

        response = self.client.delete(self.notifications_controller + '/' + str(notifications[0]['id']), {},
            format=self.format, headers=headers)
        self.assertTrue(response.status_code == status.HTTP_204_NO_CONTENT)

        # delete wrong notification

        response = self.client.delete(self.notifications_controller + '/0', {},
            format=self.format, headers=headers)
        self.assertTrue(response.status_code == status.HTTP_404_NOT_FOUND)


