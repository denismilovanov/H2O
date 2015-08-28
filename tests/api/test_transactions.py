from django.conf import settings
from tests.api.test_case import MyAPITestCase
from models import *
from rest_framework import status
import json

class TransactionsTestCase(MyAPITestCase):
    def test1(self):
        authorization = self.authorization()
        headers = authorization['headers']
        session = authorization['session']

        # my supports

        supports_controller = self.supports_controller + '/my'
        response = self.client.get(supports_controller, {
            'from_date': 'now',
            'to_date': 'now',
        }, format=self.format, headers=headers)
        self.assertTrue(response.status_code == status.HTTP_200_OK)

        supports = json.loads(response.content)
        print supports

        # my follows supports

        supports_controller = self.supports_controller + '/follows'
        response = self.client.get(supports_controller, {
            'from_date': 'now',
            'to_date': 'now',
        }, format=self.format, headers=headers)
        self.assertTrue(response.status_code == status.HTTP_200_OK)

        supports = json.loads(response.content)
        print supports

        # my receives

        receives_controller = self.receives_controller + '/my'
        response = self.client.get(receives_controller, {
            'from_date': 'now',
            'to_date': 'now',
        }, format=self.format, headers=headers)
        self.assertTrue(response.status_code == status.HTTP_200_OK)

        receives = json.loads(response.content)
        print receives

        # my follows receives

        receives_controller = self.receives_controller + '/follows'
        response = self.client.get(receives_controller, {
            'from_date': 'now',
            'to_date': 'now',
        }, format=self.format, headers=headers)
        self.assertTrue(response.status_code == status.HTTP_200_OK)

        receives = json.loads(response.content)
        print receives





