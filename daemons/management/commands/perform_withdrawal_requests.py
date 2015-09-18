from django.core.management.base import BaseCommand, CommandError
from components.queue import Queue

class Command(BaseCommand):
    help = 'Perform withdrawals'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        def handler(queue_record):
            # send one email
            from tasks.perform_withdrawal_request_task import PerformWithdrawalRequestTask
            PerformWithdrawalRequestTask.create_from_queue_task(queue_record).run()

        # sub
        Queue.subscribe('perform_withdrawal_requests', handler)
