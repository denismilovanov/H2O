from django.conf import settings
from tests.api.test_case import MyAPITestCase
from models import *
from rest_framework import status
import json

class WithdrawalsTestCase(MyAPITestCase):
    def post_withdrawal(self, email, amount, headers):
        response = self.client.post(self.withdrawals_controller, {
            'provider': 'paypal',
            'email': email,
            'amount': amount,
            'currency': 'usd',
        }, format=self.format, headers=headers)
        return response.status_code

    def test1(self):
        authorization = self.authorization(4)
        headers = authorization['headers']
        session = authorization['session']

        balance1 = self.get_balance(headers)

        amount = 1

        code = self.post_withdrawal('milovanov@octabrain.com', amount, headers)
        self.assertTrue(code == status.HTTP_201_CREATED)

        balance2 = self.get_balance(headers)

        self.assertTrue(balance1 - amount == balance2)



