from django.core.management.base import BaseCommand, CommandError
from components.queue import Queue

class Command(BaseCommand):
    help = 'Send exceptions'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        def handler(queue_record):
            # send one email
            from tasks.send_exception_task import SendExceptionTask
            SendExceptionTask.create_from_queue_task(queue_record).run()

        # sub
        Queue.subscribe('send_exceptions', handler)
