from components.emailer import Emailer, EmailerException
from jinja2 import Template, Environment, FileSystemLoader

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SendExceptionTask:
    # constructor for using in models
    def __init__(self, exception):
        self.exception = exception
        self.queue_task = None

    # method to create instance in services from raw json taken from rabbit
    @staticmethod
    def create_from_queue_task(queue_task):
        task = SendExceptionTask(queue_task.task_data['exception'])
        task.queue_task = queue_task
        return task

    # for enqueue
    def get(self):
        return {
            'exception': {
                'exception': str(self.exception),
                'traceback': self.exception.traceback,
            },
        }

    # enqueue
    def enqueue(self):
        # get trace
        try:
            import traceback
            self.exception.traceback = traceback.format_exc()
        except Exception, e:
            logger.warn(e)
            pass

        # push
        try:
            from components.queue import Queue
            Queue.push('send_exceptions', self.get())
        except Exception, e:
            logger.warn(e)
            pass

    # run this kind of tasks
    def run(self, email=None):
        try:
            #
            emailer = Emailer.get_local()
            #
            exception = self.exception
            traceback = ''
            try:
                traceback = exception.traceback
            except:
                pass

            # template
            exception = SendExceptionTask.template().render(
                exception=exception['exception'],
                traceback=exception['traceback']
            )
            # send
            from H2O.settings import DEVELOPER_EMAIL
            if not email:
                email = DEVELOPER_EMAIL

            emailer.send(email, exception, 'Exception')
            # remove task
            self.queue_task.commit()
        except EmailerException, e:
            #
            logger.warn(e)
            # delay task
            self.queue_task.rollback(60)
            return False

        return True

    # static property
    template_object = None

    # tempating
    @staticmethod
    def template():
        if SendExceptionTask.template_object:
            return SendExceptionTask.template_object

        from H2O.settings import BASE_DIR
        j2_env = Environment(loader=FileSystemLoader(BASE_DIR + '/resources/emails_templates/'), trim_blocks=True)
        # cache it
        SendExceptionTask.template_object = j2_env.get_template('exception.html')
        # return it
        return SendExceptionTask.template_object
