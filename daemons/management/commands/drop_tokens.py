from django.core.management.base import BaseCommand, CommandError
from models.user_session import UserSession
from models.user_device import UserDevice

class Command(BaseCommand):
    help = 'Drop tokens'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        UserSession.drop_access_tokens()
        UserSession.drop_refresh_tokens()
        UserDevice.drop_push_tokens()
