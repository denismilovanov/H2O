from decorators import *
from models.invite import Invite
from models.exceptions import InviteCodeAlreadyTakenException, FacebookException, NotImplementedException
from models.facebook_wrapper import FacebookWrapper

import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class User:
    # get names from social network
    @staticmethod
    def get_user_via_network(network_id, user_id, access_token):
        if network_id == 1:
            return FacebookWrapper.get_user_data(access_token)
        else:
            raise NotImplementedException('Not implemented, network_id = ' + str(network_id))


    # create or select user by network credentials
    @staticmethod
    @raw_queries()
    def upsert(user_data, network_id, user_id, access_token, invite_code, db):
        # search
        user_uuid = db.select_field('''
            SELECT main.find_user_by_network(%(network_id)s, %(user_id)s);
        ''', network_id=network_id, user_id=user_id)
        logger.debug(user_uuid)

        is_new = False

        if not user_uuid:
            # new account
            invite = Invite.get_invite_code(invite_code)
            logger.debug(invite)

            if invite['is_used']:
                # invite is used
                raise InviteCodeAlreadyTakenException('Invite code is already used')

            # create
            user_uuid = db.select_field('''
                SELECT main.add_user(%(first_name)s, %(last_name)s);
            ''', first_name=user_data['first_name'], last_name=user_data['last_name'])
            logger.debug(user_uuid)

            # add network
            db.select_field('''
                SELECT main.add_user_network(%(user_uuid)s, %(network_id)s, %(user_id)s, %(access_token)s);
            ''', user_uuid=user_uuid, network_id=network_id, user_id=user_id, access_token=access_token)

            is_new = True

            Invite.use_invite_code(invite_code, user_uuid)

        return {
            'user_uuid': user_uuid,
            'is_new': is_new,
        }

    @staticmethod
    @raw_queries()
    def get_session(user_uuid, db):
        access_token = db.select_field('''
            SELECT main.get_access_token(%(user_uuid)s);
        ''', user_uuid=user_uuid)
        logger.debug(access_token)

        refresh_token = db.select_field('''
            SELECT main.get_refresh_token(%(user_uuid)s);
        ''', user_uuid=user_uuid)
        logger.debug(refresh_token)

        return {
            'access_token': access_token,
            'refresh_token': refresh_token,
        }

    @staticmethod
    @raw_queries()
    def find_by_access_token(access_token, db):
        uuid = db.select_field('''
            SELECT main.get_user_uuid_by_access_token(%(access_token)s);
        ''', access_token=access_token)
        logger.debug(uuid)

        if not uuid:
            return None

        return User.find_by_user_uuid(uuid, 'all')

    @staticmethod
    def scope(scope):
        if scope == 'public_profile':
            return ', '.join(['uuid', 'first_name', 'last_name'])
        else:
            return '*'

    @staticmethod
    @raw_queries()
    def find_by_user_uuid(user_uuid, scope, db):
        user = db.select_record('''
            SELECT ''' + User.scope(scope) + ''' FROM main.get_user_by_uuid(%(user_uuid)s);
        ''', user_uuid=user_uuid)
        logger.debug(user)

        if not user['uuid']:
            return None

        return user

    @staticmethod
    @raw_queries()
    def refresh_access_token(refresh_token, db):
        access_token = db.select_field('''
            SELECT main.refresh_access_token(%(refresh_token)s);
        ''', refresh_token=refresh_token)
        logger.debug(refresh_token)

        return access_token

    @staticmethod
    @raw_queries()
    def drop_access_tokens(db):
        pass

    @staticmethod
    @raw_queries()
    def drop_refresh_tokens(db):
        pass
