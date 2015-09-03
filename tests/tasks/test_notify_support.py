from django.test import SimpleTestCase
from components.queue import MockTask
from tasks.notify_support_task import NotifySupportTask

class NotifySupportTestCase(SimpleTestCase):
    def test1(self):
        mock = MockTask({
            'user_id': -1,
            'counter_user_id': -2,
            'amount': 777,
            'currency': 'usd',
            'is_anonymous': False,
        })

        task = NotifySupportTask.create_from_queue_task(mock)
        result = task.run()

        self.assertTrue(result)


