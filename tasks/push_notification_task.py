from components.pusher import Pusher, PusherException

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PushNotificationTask:
    # constructor for using in models
    def __init__(self, user_id, data):
        self.user_id = user_id
        self.data = data
        self.queue_task = None

    # method to create instance in services from raw json taken from rabbit
    @staticmethod
    def create_from_queue_task(queue_task):
        task = PushNotificationTask(
            queue_task.task_data['user_id'],
            queue_task.task_data['data']
        )
        task.queue_task = queue_task
        return task

    # for enqueue
    def get(self):
        return {
            'user_id': self.user_id,
            'data': self.data,
        }

    # enqueue
    def enqueue(self):
        from components.queue import Queue
        Queue.push('push_notifications', self.get())

    # run this kind of tasks
    def run(self):
        from models.user import User
        devices = User.get_devices(self.user_id)

        logger.info('Need to push to devices, user = ' + str(self.user_id) + ':')
        logger.info(devices)

        sent = False
        if len(devices) == 0:
            sent = True

        for device in devices:
            try:
                push_token = device['push_token']
                device_type = device['device_type']
                data = self.data
                # pusher
                pusher = Pusher.get_pusher(device_type)
                # push
                pusher.push(self.user_id, push_token, data)
                #
                sent = True
            except PusherException, e:
                logger.warn(e)
                pass

        if sent:
            # remove task
            self.queue_task.commit()
        else:
            # delay task
            self.queue_task.rollback(60)
            return False

        return sent

