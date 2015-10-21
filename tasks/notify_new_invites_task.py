from models.notification import Notification
from models.user import User

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class NotifyNewInvitesTask:
    # constructor for using in models
    def __init__(self, user_id, invites_count):
        self.user_id = user_id
        self.invites_count = invites_count
        self.queue_task = None

    # method to create instance in services from raw json taken from rabbit
    @staticmethod
    def create_from_queue_task(queue_task):
        task = NotifyNewInvitesTask(queue_task.task_data['user_id'], queue_task.task_data['invites_count'])
        task.queue_task = queue_task
        return task

    # for enqueue
    def get(self):
        return {
            'user_id': self.user_id,
            'invites_count': self.invites_count,
        }

    # enqueue
    def enqueue(self):
        from components.queue import Queue
        Queue.push('notify_new_invites', self.get())

    # run this kind of tasks
    def run(self):
        # to whom
        user_id = self.user_id

        #
        logger.info('Run new_invites_available ' + str(user_id))

        try:
            # insert into db
            notification_id = Notification.add_notification(user_id, 'new_invites_available', self.get(), None)
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
