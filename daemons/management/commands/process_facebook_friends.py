from django.core.management.base import BaseCommand, CommandError
from components.queue import Queue

class Command(BaseCommand):
    help = 'Follow facebooks friends at registration'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        def handler(queue_record):
            from tasks.process_facebook_friends_task import ProcessFacebookFriendsTask
            ProcessFacebookFriendsTask.create_from_queue_task(queue_record).run()

        # sub
        Queue.subscribe('process_facebook_friends', handler)
