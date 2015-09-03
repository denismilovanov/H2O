from models.notification import Notification

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class NotifyFollowTask:
    # constructor for using in models
    def __init__(self, user_id, follow_user_id):
        self.user_id = user_id
        self.follow_user_id = follow_user_id
        self.queue_task = None

    # method to create instance in services from raw json taken from rabbit
    @staticmethod
    def create_from_queue_task(queue_task):
        task = NotifyFollowTask(queue_task.task_data['user_id'], queue_task.task_data['follow_user_id'])
        task.queue_task = queue_task
        return task

    # for enqueue
    def get(self):
        return {
            'user_id': self.user_id,
            'follow_user_id': self.follow_user_id,
        }

    # enqueue
    def enqueue(self):
        from components.queue import Queue
        Queue.push('notify_follows', self.get())

    # run this kind of tasks
    def run(self):
        # to whom
        user_id = self.user_id
        counter_user_id = self.follow_user_id

        #
        logger.info('Run somebody_follows_me ' + str(counter_user_id) + ' follows ' + str(user_id))

        try:
            # insert into db
            notification_id = Notification.add_notification(user_id, 'somebody_follows_me', self.get(), counter_user_id)
            #
            logger.info('Created notification ' + str(notification_id))

            #
            notification = Notification.get_notification_for_push(user_id, notification_id)

            # push
            from tasks.push_notification_task import PushNotificationTask
            PushNotificationTask(user_id, notification).enqueue()
        except Exception, e:
            logger.warn(e)

        # commit
        self.queue_task.commit()

        return True
