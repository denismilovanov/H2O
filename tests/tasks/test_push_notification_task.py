from django.test import SimpleTestCase
from components.queue import MockTask
from tasks.push_notification_task import PushNotificationTask

class PushNotificationTestCase(SimpleTestCase):
    def test1(self):
        mock = MockTask({
            'user_id': -1,
            'data': {
                'test_data': 'test_data'
            }
        })

        task = PushNotificationTask.create_from_queue_task(mock)
        result = task.run()

        self.assertTrue(result)

