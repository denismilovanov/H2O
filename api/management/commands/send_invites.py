from django.core.management.base import BaseCommand, CommandError
from components.queue import Queue
from components.emailer import Emailer

class Command(BaseCommand):
    help = 'Send invites'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        # emailer for everything
        emailer = Emailer.get()

        def handler(queue_record):
            # send one email
            from tasks.send_invite_task import SendInviteTask
            SendInviteTask.create_from_queue_task(queue_record).run(emailer)

        # sub
        Queue.subscribe('send_invites', handler)
