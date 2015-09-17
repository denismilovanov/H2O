from django.conf import settings
from tests.api.test_case import MyAPITestCase
from models import *
from rest_framework import status
from H2O.settings import DEVELOPER_EMAIL
import json

class WithdrawalRequestsTestCase(MyAPITestCase):
    def post_paypal_withdrawal(self, email, amount, headers):
        response = self.client.post(self.withdrawal_requests_controller, {
            'provider': 'paypal',
            'email': email,
            'amount': amount,
            'currency': 'usd',
        }, format=self.format, headers=headers)
        return response.status_code

    def get_withdrawal_requests(self, headers):
        response = self.client.get(self.withdrawal_requests_controller, {}, format=self.format, headers=headers)
        self.assertTrue(response.status_code == status.HTTP_200_OK)
        return json.loads(response.content)

    def test1(self):
        authorization = self.authorization(4)
        headers = authorization['headers']
        session = authorization['session']

        balance1 = self.get_balance(headers)

        amount = 1
        email = DEVELOPER_EMAIL

        code = self.post_paypal_withdrawal(email, amount, headers)
        self.assertTrue(code == status.HTTP_201_CREATED)

        # large amount of money
        code = self.post_paypal_withdrawal(email, 1e7, headers)
        self.assertTrue(code == status.HTTP_406_NOT_ACCEPTABLE)

        # wrong email
        code = self.post_paypal_withdrawal('WRONG_EMAIL', amount, headers)
        self.assertTrue(code == status.HTTP_400_BAD_REQUEST)

        balance2 = self.get_balance(headers)

        # there is no real w/d
        self.assertTrue(balance1 == balance2)

        # requests list
        requests = self.get_withdrawal_requests(headers)
        self.assertTrue(requests[0]['amount'] == amount)


