from models.withdrawal_request import WithdrawalRequest

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PerformWithdrawalRequestTask:
    # constructor for using in models
    def __init__(self, user_id, withdrawal_request_id):
        self.user_id = user_id
        self.withdrawal_request_id = withdrawal_request_id
        self.queue_task = None

    # method to create instance in services from raw json taken from rabbit
    @staticmethod
    def create_from_queue_task(queue_task):
        task = PerformWithdrawalRequestTask(queue_task.task_data['user_id'], queue_task.task_data['withdrawal_request_id'])
        task.queue_task = queue_task
        return task

    # for enqueue
    def get(self):
        return {
            'user_id': self.user_id,
            'withdrawal_request_id': self.withdrawal_request_id,
        }

    # enqueue
    def enqueue(self):
        from components.queue import Queue
        Queue.push('perform_withdrawal_requests', self.get())

    # run this kind of tasks
    def run(self):
        # data
        user_id = self.user_id
        withdrawal_request_id = self.withdrawal_request_id
        user = User.get_by_id(user_id, scope='all')

        #
        logger.info('Run perform_withdrawal_requests ' + str(user_id) + \
                    ' withdrawal_request_id ' + str(withdrawal_request_id))

        # withdrawal_request = WithdrawalRequest

        # commit
        self.queue_task.commit()

        return True
