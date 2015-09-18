from django.test import TestCase
from components.queue import MockTask
from tasks.perform_withdrawal_request_task import PerformWithdrawalRequestTask
from H2O.settings import DEBUG

class PerformWithdrawalRequestTaskTestCase(TestCase):
    def test1(self):
        # performing this task in prod will cause real money movement
        if not DEBUG:
            return

        mock = MockTask({
            'user_id': -1,
            # special test w/d request
            'withdrawal_request_id': -1,
        })

        task = PerformWithdrawalRequestTask.create_from_queue_task(mock)
        result = task.run()

        self.assertTrue(result)

