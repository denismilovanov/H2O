from decorators import *

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
