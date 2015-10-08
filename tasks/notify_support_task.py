from models.notification import Notification
from models.user import User

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class NotifySupportTask:
    # constructor for using in models
    def __init__(self, user_id, counter_user_id, amount, currency, is_anonymous):
        self.user_id = user_id
        self.counter_user_id = counter_user_id
        self.amount = amount
        self.currency = currency
        self.is_anonymous = is_anonymous
        self.queue_task = None

    # method to create instance in services from raw json taken from rabbit
    @staticmethod
    def create_from_queue_task(queue_task):
        task = NotifySupportTask(
            queue_task.task_data['user_id'],
            queue_task.task_data['counter_user_id'],
            queue_task.task_data['amount'],
            queue_task.task_data['currency'],
            queue_task.task_data['is_anonymous']
        )
        task.queue_task = queue_task
        return task

    # for enqueue
    def get(self):
        return {
            'user_id': self.user_id,
            'counter_user_id': self.counter_user_id,
            'amount': self.amount,
            'currency': self.currency,
            'is_anonymous': self.is_anonymous,
        }

    # enqueue
    def enqueue(self):
        from components.queue import Queue
        Queue.push('notify_supports', self.get())

    # run this kind of tasks
    def run(self):
        # to whom
        user_id = self.user_id
        counter_user_id = self.counter_user_id
        # user
        user = User.get_by_id(user_id, scope='all')
        if not user:
            # it can happend in tests:
            # user is not present in db already, but the task in rabbit is
            self.queue_task.commit()
            return True

        #
        logger.info('Run somebody_sent_me_money ' + str(counter_user_id) + ' supports ' + str(user_id))

        data = {
            'amount': self.amount,
            'currency': self.currency,
            'is_anonymous': self.is_anonymous,
        }

        try:
            # insert into db
            notification_id = Notification.add_notification(user_id, 'somebody_sent_me_money', data, counter_user_id)
            #
            logger.info('Created notification ' + str(notification_id))

            #
            notification = Notification.get_notification_for_push(user_id, notification_id)

            # push
            from tasks.push_notification_task import PushNotificationTask
            PushNotificationTask(user_id, notification).enqueue()
        except Exception, e:
            logger.warn(e)
            from tasks.send_exception_task import send_exception
            send_exception(e)

        # commit
        self.queue_task.commit()

        return True
