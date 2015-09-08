from tasks.send_exception_task import SendExceptionTask
from django.test import SimpleTestCase
from components.queue import MockTask
import traceback

class SendAlertTestCase(SimpleTestCase):
    def test1(self):

        try:
            a = 1 / 0

        except Exception, e:
            e.traceback = traceback.format_exc()

            mock = MockTask({
                'exception': {
                    'exception': str(e),
                    'traceback': e.traceback,
                },
            })

            task = SendExceptionTask.create_from_queue_task(mock)
            result = task.run('TEST_EMAIL_developer@octabrain.com')
            self.assertTrue(result)



