from django.conf import settings
from tests.api.test_case import MyAPITestCase
from models import *
from rest_framework import status
import json

class TransactionsTestCase(MyAPITestCase):
    def get_balance(self, headers):
        user_controller = self.user_controller + 'me'
        response = self.client.get(user_controller, {}, format=self.format, headers=headers)
        self.assertTrue(response.status_code == status.HTTP_200_OK)
        balance = json.loads(response.content)['balance']
        return balance

    def test1(self):
        authorization = self.authorization()
        headers = authorization['headers']
        session = authorization['session']

        # balance
        balance1 = self.get_balance(headers)

        # do support

        amount = 10

        supports_controller = self.supports_controller
        response = self.client.post(supports_controller, {
            'amount': amount,
            'uuid': '00000009-0000-0000-0000-000000000009',
            'currency': 'usd',
            'is_anonymous': True,
        }, format=self.format, headers=headers)
        self.assertTrue(response.status_code == status.HTTP_201_CREATED)

        supports = json.loads(response.content)

        # balance
        balance2 = self.get_balance(headers)

        # check balances
        self.assertTrue(balance1 - amount == balance2)

        # stat

        statistics_controller = self.statistics_controller + '/my/overall'
        response = self.client.get(statistics_controller, {}, format=self.format, headers=headers)
        self.assertTrue(response.status_code == status.HTTP_200_OK)
        stat = json.loads(response.content)

        statistics_controller = self.statistics_controller + '/my/counter_users/supports'
        response = self.client.get(statistics_controller, {}, format=self.format, headers=headers)
        self.assertTrue(response.status_code == status.HTTP_200_OK)
        stat = json.loads(response.content)

        # my supports

        supports_controller = self.supports_controller + '/my'
        response = self.client.get(supports_controller, {
            'from_date': 'now',
            'to_date': 'now',
        }, format=self.format, headers=headers)
        self.assertTrue(response.status_code == status.HTTP_200_OK)
        supports = json.loads(response.content)

        # my follows supports

        supports_controller = self.supports_controller + '/follows'
        response = self.client.get(supports_controller, {
            'from_date': 'now',
            'to_date': 'now',
        }, format=self.format, headers=headers)
        self.assertTrue(response.status_code == status.HTTP_200_OK)

        supports = json.loads(response.content)

        # my receives

        receives_controller = self.receives_controller + '/my'
        response = self.client.get(receives_controller, {
            'from_date': 'now',
            'to_date': 'now',
        }, format=self.format, headers=headers)
        self.assertTrue(response.status_code == status.HTTP_200_OK)

        receives = json.loads(response.content)

        # my follows receives

        receives_controller = self.receives_controller + '/follows'
        response = self.client.get(receives_controller, {
            'from_date': 'now',
            'to_date': 'now',
        }, format=self.format, headers=headers)
        self.assertTrue(response.status_code == status.HTTP_200_OK)

        receives = json.loads(response.content)

        # my transactions = supports + receives

        transactions_controller = self.transactions_controller + '/my'
        response = self.client.get(transactions_controller, {
            'limit': 10,
            'offset': 0,
        }, format=self.format, headers=headers)
        self.assertTrue(response.status_code == status.HTTP_200_OK)

        transactions = json.loads(response.content)

        # follows transactions = supports + receives

        transactions_controller = self.transactions_controller + '/follows'
        response = self.client.get(transactions_controller, {
            'limit': 10,
            'offset': 0,
        }, format=self.format, headers=headers)
        self.assertTrue(response.status_code == status.HTTP_200_OK)

        transactions = json.loads(response.content)



