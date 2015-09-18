from decorators import *
from models.exceptions import InvalidEmail, EmailIsAlreadyUsed

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Invite:
    @staticmethod
    @raw_queries()
    def get_invite_code(invite_code, db):
        code = db.select_record('''
            SELECT * FROM main.get_invite_code(%(invite_code)s);
        ''', invite_code=invite_code)

        if not code['invite_code']:
            return None

        return code

    @staticmethod
    def use_invite_code(user_id, invite_code, db):
        db.select_field('''
            SELECT main.use_invite_code(%(invite_code)s, %(user_id)s);
        ''', invite_code=invite_code, user_id=user_id)

        return True

    @staticmethod
    @raw_queries()
    def send_invite_code(invite_code, db):
        db.select_field('''
            SELECT main.send_invite_code(%(invite_code)s);
        ''', invite_code=invite_code)

        return True

    @staticmethod
    def scope(scope):
        if scope == 'public_invite_codes':
            return ', '.join(['invite_code', 'status', 'email', 'entrance_gift'])
        else:
            return '*'

    @staticmethod
    @raw_queries()
    def get_invite_codes_by_user_id(user_id, scope, db):
        codes = db.select_table('''
            SELECT ''' + Invite.scope(scope) + ''' FROM main.get_invite_codes_by_user_id(%(user_id)s);
        ''', user_id=user_id)

        return codes

    @staticmethod
    def create_invite_codes_for_user_id(user_id, count, db):
        db.select_field('''
            SELECT main.create_invite_codes_for_user_id(%(user_id)s, %(count)s);
        ''', user_id=user_id, count=count);

        return True

    @staticmethod
    @raw_queries()
    def invite_user_via_invite_code_and_email(invite_code, email, entrance_gift, db):
        logger.info('invite_user_via_invite_code_and_email')
        logger.info(str(invite_code) + ' ' + str(email) + ' ' + str(entrance_gift))

        from validate_email import validate_email
        if not email or not validate_email(email):
            raise InvalidEmail()

        try:
            db.select_field('''
                SELECT main.invite_user_via_invite_code_and_email(%(invite_code)s, %(email)s, %(entrance_gift)s);
            ''', invite_code=invite_code, email=email, entrance_gift=entrance_gift)
        except Exception, e:
            raise EmailIsAlreadyUsed()

        # sending though queue
        try:
            from tasks.send_invite_task import SendInviteTask
            SendInviteTask(email, invite_code).enqueue()
        except Exception, e:
            # there is no need to raise exception and scare user
            # we shall perform regular checks of codes without sent emails
            logger.info(e)

        return True
