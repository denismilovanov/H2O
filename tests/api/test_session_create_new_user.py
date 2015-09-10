from django.conf import settings
from tests.api.test_case import MyAPITestCase
from models import *
from rest_framework import status
import json

class SessionCreateNewUserTestCase(MyAPITestCase):
    def test1(self):
        token = 'CAAGm0PX4ZCpsBAIc08Q3AvKdQ8TjoUbIPK5Y8Uu9LlKddpKZAkxrCZBYvj5Lyrgoha5anxyTah5YgfNDt67zJNwa1ZC6HQoEkfOrmkGeZAW1qgCIApSpcAL7ZC4PquPhbZBrH4TbjRhohvSi2BWwUKLiyqiSx4UfpEZA6DZAvdmxXXyu4RTj56qNXBTUhlBIZCplyG0wzUQFQhIwZDZD'

        authorization = self.authorization(None, token)
        headers = authorization['headers']
        session = authorization['session']

        self.assertTrue(session['user']['is_new'])
