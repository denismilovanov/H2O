from django.core.management.base import BaseCommand, CommandError
from components.queue import Queue

class Command(BaseCommand):
    help = 'Notify about follows'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        def handler(queue_record):
            # send one email
            from tasks.notify_follow_task import NotifyFollowTask
            NotifyFollowTask.create_from_queue_task(queue_record).run()

        # sub
        Queue.subscribe('notify_follows', handler)
