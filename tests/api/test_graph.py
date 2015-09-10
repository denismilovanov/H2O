from django.conf import settings
from tests.api.test_case import MyAPITestCase
from models import *
from rest_framework import status
import json

class GraphTestCase(MyAPITestCase):
    def test1(self):
        headers = self.authorization()['headers']

        response = self.client.get(self.graph_controller, {}, format=self.format, headers=headers)
        self.assertTrue(response.status_code == status.HTTP_200_OK)


