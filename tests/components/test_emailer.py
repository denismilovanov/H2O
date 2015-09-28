from components.emailer import Emailer
from H2O.settings import DEVELOPER_EMAIL
from django.test import SimpleTestCase


class QueueTestCase(SimpleTestCase):
    def test1(self):
        emailer = Emailer.get()

        self.assertTrue(emailer.send(DEVELOPER_EMAIL, 'Hello from test.', 'Mandrill test'))





