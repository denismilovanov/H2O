from components.emailer import Emailer, EmailerException
from models import Invite
from jinja2 import Template, Environment, FileSystemLoader

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SendInviteTask:
    # constructor for using in models
    def __init__(self, email, invite_code):
        self.email = email
        self.invite_code = invite_code
        self.queue_task = None

    # method to create instance in services from raw json taken from rabbit
    @staticmethod
    def create_from_queue_task(queue_task):
        task = SendInviteTask(queue_task.task_data['email'], queue_task.task_data['invite_code'])
        task.queue_task = queue_task
        return task

    # for push
    def get(self):
        return {
            'email': self.email,
            'invite_code': self.invite_code,
        }

    # push
    def push(self):
        from components.queue import Queue
        Queue.push('send_invites', self.get())

    # run this kind of tasks
    def run(self, emailer):
        try:
            email = self.email
            invite_code = self.invite_code
            # template
            invite = SendInviteTask.template().render(invite_code=invite_code)
            # send
            emailer.send(email, invite)
            # change status
            Invite.send_invite_code(invite_code)
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
        if SendInviteTask.template_object:
            return SendInviteTask.template_object

        from H2O.settings import BASE_DIR
        j2_env = Environment(loader=FileSystemLoader(BASE_DIR + '/resources/emails_templates/'), trim_blocks=True)
        # cache it
        SendInviteTask.template_object = j2_env.get_template('invite.html')
        # return it
        return SendInviteTask.template_object
