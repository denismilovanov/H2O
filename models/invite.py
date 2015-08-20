from decorators import *
from models.exceptions import InvalidEmail, EmailIsAlreadyUsed

import logging
logging.basicConfig(level=logging.DEBUG)
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
    @raw_queries()
    def use_invite_code(invite_code, user_uuid, db):
        db.select_field('''
            SELECT main.use_invite_code(%(invite_code)s, %(user_uuid)s);
        ''', invite_code=invite_code, user_uuid=user_uuid)

        return True

    @staticmethod
    def scope(scope):
        if scope == 'public_invite_codes':
            return ', '.join(['invite_code', 'status', 'email'])
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
    @raw_queries()
    def create_invite_codes_for_user_id(user_id, count, db):
        db.select_field('''
            SELECT main.create_invite_codes_for_user_id(%(user_id)s, %(count)s);
        ''', user_id=user_id, count=count);

        return True

    @staticmethod
    @raw_queries()
    def invite_user_via_invite_code_and_email(invite_code, email, db):
        logger.debug('invite_user_via_invite_code_and_email')
        logger.debug(str(invite_code) + ' ' + str(email))

        from validate_email import validate_email
        if not email or not validate_email(email):
            raise InvalidEmail()

        try:
            db.select_field('''
                SELECT main.invite_user_via_invite_code_and_email(%(invite_code)s, %(email)s);
            ''', invite_code=invite_code, email=email)
        except Exception, e:
            raise EmailIsAlreadyUsed()

        return True
