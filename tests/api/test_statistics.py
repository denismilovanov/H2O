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

        # other

        statistics_controller = self.statistics_controller + '/my/counter_users/receives'
        response = self.client.get(statistics_controller, {}, format=self.format, headers=headers)
        self.assertTrue(response.status_code == status.HTTP_200_OK)

        # follow statistics

        statistics_controller = self.statistics_controller + '/00000002-0000-0000-0000-000000000002/overall'
        response = self.client.get(statistics_controller, {}, format=self.format, headers=headers)
        self.assertTrue(response.status_code == status.HTTP_200_OK)
        print response.content

        # follow counter users statistics

        statistics_controller = self.statistics_controller + '/00000002-0000-0000-0000-000000000002/counter_users/receives'
        response = self.client.get(statistics_controller, {}, format=self.format, headers=headers)
        self.assertTrue(response.status_code == status.HTTP_200_OK)
        print response.content






