from django.conf import settings
from tests.api.test_case import MyAPITestCase
from models import *
from rest_framework import status
import json

class DepositsTestCase(MyAPITestCase):
    def post_deposit(self, provider_transaction_id, amount, headers):
        response = self.client.post(self.deposits_controller, {
            'provider': 'paypal',
            'provider_transaction_id': provider_transaction_id,
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

        code = self.post_deposit('PAY-8TK27125MK966472MKXZLDBY', amount, headers)
        self.assertTrue(code == status.HTTP_201_CREATED)

        code = self.post_deposit('PAY-8TK27125MK966472MKXZLDBY', amount, headers)
        self.assertTrue(code == status.HTTP_409_CONFLICT)

        code = self.post_deposit('PAY-ZZZZZZZZZZZZZZZZZZZZZZZZ', amount, headers)
        self.assertTrue(code == status.HTTP_406_NOT_ACCEPTABLE)

        balance2 = self.get_balance(headers)

        self.assertTrue(balance1 + amount == balance2)



