from django.conf import settings
from tests.api.test_case import MyAPITestCase
from models import *
from rest_framework import status
import json

class SessionCreateNewUserTestCase(MyAPITestCase):
    def test1(self):
        token = self.get_facebook_access_token()

        authorization = self.authorization(None, token)
        headers = authorization['headers']
        session = authorization['session']

        self.assertTrue(session['user']['is_new'])
