from components.pusher import Pusher

from django.test import SimpleTestCase
from models import *


class IOSPusherTestCase(SimpleTestCase):
    def test1(self):
        token = '89daa349b32514b539b035f12bf20c26ad0e2825512f18e3762b64da2454a022'
        Pusher.get_pusher('ios').push(None, token, {'push_header': 'header', 'bla': 'text', 'inner': {'go_deeper': '1'}})



