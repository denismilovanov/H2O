from components.emailer import Emailer, EmailerException
from models import Invite, User
from jinja2 import Template, Environment, FileSystemLoader
from H2O.settings import CONTACT_EMAIL, BASE_URL

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

    # for enqueue
    def get(self):
        return {
            'email': self.email,
            'invite_code': self.invite_code,
        }

    # enqueue
    def enqueue(self):
        from components.queue import Queue
        Queue.push('send_invites', self.get())

    # run this kind of tasks
    def run(self):
        try:
            #
            emailer = Emailer.get()
            #
            email = self.email
            invite_code = self.invite_code

            #
            invite = Invite.get_invite_code(invite_code)
            owner = User.get_by_id(invite['owner_id'], scope='all')
            owner_name = owner['name']
            owner_avatar_url = owner['avatar_url']
            if not owner['id']:
                # anonymous -> team
                owner_name = 'H2O team'
                owner_avatar_url = BASE_URL + '/images/team.png'

            # template
            invite = SendInviteTask.template().render(
                invite_code=invite_code,
                owner_name=owner_name,
                owner_avatar_url=owner_avatar_url,
                contact_email=CONTACT_EMAIL,
                email=email,
            )
            # send
            emailer.send(email, invite, owner_name + ' invited you to join Hearts2Open community')
            # do not change status of test code
            if not invite_code.startswith('TEST_INVITE_CODE'):
                # change status
                Invite.send_invite_code(invite_code)

            # remove task
            self.queue_task.commit()
        except EmailerException, e:
            #
            logger.warn(e)

            # notify dev
            from tasks.send_exception_task import send_exception
            send_exception(e)

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
