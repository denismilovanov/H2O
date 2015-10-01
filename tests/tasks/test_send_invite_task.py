from tasks.send_invite_task import SendInviteTask
from django.test import SimpleTestCase
from components.queue import MockTask
from components.emailer import Emailer

class SendInviteTestCase(SimpleTestCase):
    def test1(self):
        from H2O.settings import TEST_INVITE_CODE
        mock = MockTask({
            'email': 'TEST_EMAIL_me@denismilovanov.net',
            'invite_code': TEST_INVITE_CODE,
        })

        task = SendInviteTask.create_from_queue_task(mock)
        result = task.run()
        self.assertTrue(result)


