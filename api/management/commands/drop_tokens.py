from django.core.management.base import BaseCommand, CommandError
from models.user_session import UserSession

class Command(BaseCommand):
    help = 'Drop tokens'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        UserSession.drop_access_tokens()
        UserSession.drop_refresh_tokens()
