from django.core.management.base import BaseCommand, CommandError
from components.queue import Queue

class Command(BaseCommand):
    help = 'Send invites'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        def handler(queue_record):
            # send one email
            from tasks.push_notification_task import PushNotificationTask
            PushNotificationTask.create_from_queue_task(queue_record).run()

        # sub
        Queue.subscribe('push_notifications', handler)
