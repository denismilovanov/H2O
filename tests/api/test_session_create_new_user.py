from django.conf import settings
from tests.api.test_case import MyAPITestCase
from models import *
from rest_framework import status
import json
from H2O.settings import ENTRANCE_GIFT_AMOUNT

class SessionCreateNewUserTestCase(MyAPITestCase):
    def test1(self):
        token = self.get_facebook_access_token()

        # user will be created, invite code has entrance_gift attached
        authorization = self.authorization(None, token)
        headers = authorization['headers']
        session = authorization['session']

        self.assertTrue(session['user']['is_new'])

        balance = self.get_balance(headers)
        # gift
        self.assertTrue(balance == ENTRANCE_GIFT_AMOUNT)

        # follow friends sync
        # in production it will be async

        from components.queue import MockTask
        mock = MockTask({
            'user_id': User.extract_user_id_from_uuid(session['user']['uuid']),
            'access_token': token,
            'type': 'follow_friends',
        })

        from tasks import ProcessFacebookFriendsTask
        task = ProcessFacebookFriendsTask.create_from_queue_task(mock)
        result = task.run()
