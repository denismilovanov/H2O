from decorators import *
from models.exceptions import InviteCodeDoesNotExistException

class Invite:
    @staticmethod
    @raw_queries()
    def get_invite_code(invite_code, db):
        code = db.select_record('''
            SELECT * FROM main.get_invite_code(%(invite_code)s);
        ''', invite_code=invite_code)

        if not code['code']:
            raise InviteCodeDoesNotExistException()

        return code

    @staticmethod
    @raw_queries()
    def use_invite_code(invite_code, user_uuid, db):
        db.select_field('''
            SELECT main.use_invite_code(%(invite_code)s, %(user_uuid)s);
        ''', invite_code=invite_code, user_uuid=user_uuid)

        return True
