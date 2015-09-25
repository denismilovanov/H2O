from components.pusher import Pusher

from django.test import SimpleTestCase
from models import *


class AndroidPusherTestCase(SimpleTestCase):
    def test1(self):
        token = 'Bz83t-zFXA:APA91bEu3VjBB3MamkjyOL0rEeWb64F1Qttq9dva87nI-Uu8cCm-bAkj3qr05wQWJ27wj5Z1WIpXuVb8Py1mLBPVyUp4rFrS8Cr-di4xfmHnmh1KCOT6W-cEq4ITyaCQDWq4w9PNDYor'
        Pusher.get_pusher('android').push(-1, token, {'push_header': 'header', 'bla': 'text', 'inner': {'go_deeper': '1'}})


