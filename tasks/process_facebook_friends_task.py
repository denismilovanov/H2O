from models.user import User

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ProcessFacebookFriendsTask:
    # constructor for using in models
    def __init__(self, user_id, access_token, type):
        self.user_id = user_id
        self.access_token = access_token
        self.type = type
        self.queue_task = None

    # method to create instance in services from raw json taken from rabbit
    @staticmethod
    def create_from_queue_task(queue_task):
        task = ProcessFacebookFriendsTask(
            queue_task.task_data['user_id'],
            queue_task.task_data['access_token'],
            queue_task.task_data['type']
        )
        task.queue_task = queue_task
        return task

    # for enqueue
    def get(self):
        return {
            'user_id': self.user_id,
            'access_token': self.access_token,
            'type': self.type,
        }

    # enqueue
    def enqueue(self):
        from components.queue import Queue
        try:
            Queue.push('process_facebook_friends', self.get())
        except Exception, e:
            logger.warn(e)

    # run this kind of tasks
    def run(self):
        # user data
        user_id = self.user_id
        access_token = self.access_token

        # get him
        user = User.get_by_id(user_id, scope='all')
        if not user:
            # it can happend in tests:
            # user is not present in db already, but the task in rabbit is
            self.queue_task.commit()
            return True

        # FB id
        facebook_id = user['facebook_id']

        # log
        logger.info('Run process_facebook_friends ' + str(user_id))

        # get friends from FB
        from models.facebook_wrapper import FacebookWrapper
        facebook_friends_ids = FacebookWrapper.get_user_friends_ids(access_token, facebook_id)

        if facebook_friends_ids == False:
            self.queue_task.rollback(10)
            return False

        # follow them
        from models import UserFollow
        UserFollow.follow_my_facebook_fiends_by_their_ids(user_id, facebook_friends_ids)

        # commit
        self.queue_task.commit()

        return True
