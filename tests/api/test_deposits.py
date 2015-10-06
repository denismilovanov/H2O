from django.conf import settings
from tests.api.test_case import MyAPITestCase
from models import *
from rest_framework import status
import json
from H2O.settings import DEBUG
import stripe

class DepositsTestCase(MyAPITestCase):
    def post_deposit(self, provider, provider_transaction_id, provider_transaction_token, amount, headers):
        response = self.client.post(self.deposits_controller, {
            'provider': provider,
            'provider_transaction_id': provider_transaction_id,
            'provider_transaction_token': provider_transaction_token,
            'amount': amount,
            'currency': 'usd',
        }, format=self.format, headers=headers)
        return response.status_code

    def paypal(self):
        authorization = self.authorization(4)
        headers = authorization['headers']
        session = authorization['session']

        balance1 = self.get_balance(headers)

        amount = 1

        from H2O.settings import PAYPAL_SANDBOX_TRANSACTION_ID

        code = self.post_deposit('paypal', PAYPAL_SANDBOX_TRANSACTION_ID, None, amount, headers)
        self.assertTrue(code == status.HTTP_201_CREATED)

        code = self.post_deposit('paypal', PAYPAL_SANDBOX_TRANSACTION_ID, None, amount, headers)
        self.assertTrue(code == status.HTTP_409_CONFLICT)

        code = self.post_deposit('paypal', 'PAY-ZZZZZZZZZZZZZZZZZZZZZZZZ', None, amount, headers)
        self.assertTrue(code == status.HTTP_406_NOT_ACCEPTABLE)

        balance2 = self.get_balance(headers)

        self.assertTrue(balance1 + amount == balance2)

    def stripe(self):
        authorization = self.authorization(4)
        headers = authorization['headers']
        session = authorization['session']

        balance1 = self.get_balance(headers)

        amount = 2

        from H2O.settings import STRIPE_SANDBOX_CARD

        provider_transaction_token = stripe.Token.create(card={
            'number': STRIPE_SANDBOX_CARD,
            'cvc': 111,
            'exp_month': 1,
            'exp_year': 2020,
        }).id

        code = self.post_deposit('stripe', None, provider_transaction_token, amount, headers)
        self.assertTrue(code == status.HTTP_201_CREATED)

        balance2 = self.get_balance(headers)

        amount -= Transaction.calculate_stripe_fee(amount)

        self.assertTrue(balance1 + amount == balance2)


    def test1(self):
        # wrong data
        authorization = self.authorization(4)
        headers = authorization['headers']
        wrong = self.post_deposit('paypal', None, None, 0, headers)
        self.assertTrue(wrong == status.HTTP_400_BAD_REQUEST)

        # deposit method checks if given transaction exists and its params match
        # then it moves money
        # we cannot perform this operations in live mode
        if not DEBUG:
            return

        self.paypal()
        self.stripe()


