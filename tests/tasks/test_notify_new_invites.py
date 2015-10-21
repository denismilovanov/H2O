from django.test import SimpleTestCase
from components.queue import MockTask
from tasks.notify_new_invites_task import NotifyNewInvitesTask

class NotifyFollowTestCase(SimpleTestCase):
    def test1(self):
        mock = MockTask({
            'user_id': -1,
            'invites_count': 7,
        })

        task = NotifyNewInvitesTask.create_from_queue_task(mock)
        result = task.run()

        self.assertTrue(result)


