from django.test import SimpleTestCase
from components.queue import MockTask
from tasks.notify_follow_task import NotifyFollowTask

class NotifyFollowTestCase(SimpleTestCase):
    def test1(self):
        mock = MockTask({
            'user_id': -1,
            'follow_user_id': -2,
        })

        task = NotifyFollowTask.create_from_queue_task(mock)
        result = task.run()

        self.assertTrue(result)


