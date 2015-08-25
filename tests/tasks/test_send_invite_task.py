from tasks.send_invite_task import SendInviteTask
from django.test import SimpleTestCase
from components.queue import MockTask
from components.emailer import Emailer
from tasks.send_invite_task import SendInviteTask

class SendInviteTestCase(SimpleTestCase):
    def test1(self):
        mock = MockTask({
            'email': 'me@denismilovanov.net',
            'invite_code': 'Q123',
        })

        task = SendInviteTask.create_from_queue_task(mock)
        emailer = Emailer.get()
        result = task.run(emailer)

        self.assertTrue(result)
