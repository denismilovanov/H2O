from django.core.management.base import BaseCommand, CommandError
from models.user import User

class Command(BaseCommand):
    help = 'Drop tokens'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        User.drop_access_tokens()
        User.drop_refresh_tokens()
