from django.conf import settings
from tests.api.test_case import MyAPITestCase
from models import *
from rest_framework import status
import json

class TransactionsTestCase(MyAPITestCase):
    def get_stat_overall(self, headers):
        statistics_controller = self.statistics_controller + '/my/overall'
        response = self.client.get(statistics_controller, {}, format=self.format, headers=headers)
        self.assertTrue(response.status_code == status.HTTP_200_OK)
        stat = json.loads(response.content)
        return stat

    def get_stat_counter_users_supports(self, headers):
        statistics_controller = self.statistics_controller + '/my/counter_users/supports'
        response = self.client.get(statistics_controller, {}, format=self.format, headers=headers)
        self.assertTrue(response.status_code == status.HTTP_200_OK)
        stat = json.loads(response.content)
        return stat

    def get_transactions(self, who, headers):
        transactions_controller = self.transactions_controller + '/' + who
        response = self.client.get(transactions_controller, {
            'limit': 10,
            'offset': 0,
        }, format=self.format, headers=headers)
        self.assertTrue(response.status_code == status.HTTP_200_OK)
        transactions = json.loads(response.content)
        return transactions

    def post_support(self, headers, uuid, amount, is_anonymous):
        supports_controller = self.supports_controller
        response = self.client.post(supports_controller, {
            'amount': amount,
            'uuid': uuid,
            'currency': 'usd',
            'is_anonymous': is_anonymous,
        }, format=self.format, headers=headers)
        self.assertTrue(response.status_code == status.HTTP_201_CREATED)
        supports = json.loads(response.content)

    def test1(self):
        authorization = self.authorization(4)
        headers = authorization['headers']
        session = authorization['session']

        counter_authorization = self.authorization(5)
        counter_headers = counter_authorization['headers']
        counter_session = counter_authorization['session']

        # balance
        balance1 = self.get_balance(headers)

        # do supports

        amount1 = 10
        amount2 = 20
        amount3 = 50
        counter_user_uuid = '00000005-0000-0000-0000-000000000005'
        self.post_support(headers, counter_user_uuid, amount1, False)
        self.post_support(headers, counter_user_uuid, amount2, False)
        self.post_support(headers, counter_user_uuid, amount3, True)

        # balance
        balance2 = self.get_balance(headers)

        # check balances
        self.assertTrue(balance1 - amount1 - amount2 - amount3 == balance2)

        # assert stat overall

        stat = self.get_stat_overall(headers)
        self.assertTrue(stat['supports']['transactions_count'] == 3)
        self.assertTrue(stat['supports']['users_count'] == 1)

        # assert stat counters

        stat = self.get_stat_counter_users_supports(headers)
        counter_user = stat[0]
        self.assertTrue(counter_user['uuid'] == counter_user_uuid)
        self.assertTrue(counter_user['transactions_count'] == 3)

        #

        counter_stat = self.get_stat_overall(counter_headers)

        # transactions = supports + receives

        my_transactions = self.get_transactions('my', headers)

        counter_transactions = self.get_transactions('my', counter_headers)

        # follows transactions

        follows_transactions = self.get_transactions('follows', headers)





