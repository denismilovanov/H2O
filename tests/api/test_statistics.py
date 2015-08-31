from django.conf import settings
from tests.api.test_case import MyAPITestCase
from models import *
from rest_framework import status
import json

class StatisticsTestCase(MyAPITestCase):
    def test1(self):
        authorization = self.authorization()
        headers = authorization['headers']
        session = authorization['session']

        # my statistics

        statistics_controller = self.statistics_controller + '/my/overall'
        response = self.client.get(statistics_controller, {}, format=self.format, headers=headers)
        self.assertTrue(response.status_code == status.HTTP_200_OK)

        supports = json.loads(response.content)
        print supports







