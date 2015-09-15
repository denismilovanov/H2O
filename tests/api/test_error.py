from django.conf import settings
from tests.api.test_case import MyAPITestCase
from models import *
from rest_framework import status
import json

class ErrorTestCase(MyAPITestCase):
    def test1(self):
        authorization = self.authorization()
        headers = authorization['headers']
        session = authorization['session']

        response = self.client.post(self.error_controller + '/403', {}, format=self.format, headers=headers)
        self.assertTrue(response.status_code == status.HTTP_403_FORBIDDEN)



