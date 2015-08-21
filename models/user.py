from decorators import *
from models.invite import Invite
from models.user_network import UserNetwork
from models.user_session import UserSession
from models.exceptions import InviteCodeAlreadyTakenException, InviteCodeDoesNotExistException, FacebookException, NotImplementedException
from models.facebook_wrapper import FacebookWrapper

import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class User:
    # get names from social network
    @staticmethod
    def get_user_via_network(network_id, access_token):
        if str(network_id) == '1':
            return FacebookWrapper.get_user_data(access_token)
        else:
            raise NotImplementedException


    # create or select user by network credentials
    @staticmethod
    @raw_queries()
    def upsert(user_data, network_id, access_token, invite_code, db):
        logger.debug('upsert')
        logger.debug(user_data)

        user_id = user_data['id']

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

            if not invite:
                # there is no code
                raise InviteCodeDoesNotExistException

            if invite['is_used']:
                # invite is used
                raise InviteCodeAlreadyTakenException

            # create
            user_uuid = db.select_field('''
                SELECT main.upsert_user(NULL, %(name)s, %(avatar_url)s);
            ''', name=user_data['name'], avatar_url=user_data['avatar_url'])
            logger.debug(user_uuid)

            # use code
            Invite.use_invite_code(invite_code, user_uuid)

            # create codes
            user_id = db.select_field('''
                SELECT id FROM main.get_user_by_uuid(%(user_uuid)s);
            ''', user_uuid=user_uuid)
            Invite.create_invite_codes_for_user_id(user_id, 3)

            # newness flag
            is_new = True

        else:
            # update information
            db.select_field('''
                SELECT main.upsert_user(%(user_uuid)s, %(name)s, %(avatar_url)s);
            ''', user_uuid=user_uuid, name=user_data['name'], avatar_url=user_data['avatar_url'])

            # get id
            user_id = db.select_field('''
                SELECT id FROM main.get_user_by_uuid(%(user_uuid)s);
            ''', user_uuid=user_uuid)

        # upsert network
        UserNetwork.upsert_network(user_uuid, network_id, user_id, access_token)

        # that was all
        return {
            'user_uuid': user_uuid,
            'is_new': is_new,
            'avatar_url': user_data['avatar_url'],
            'name': user_data['name'],
        }, user_id

    @staticmethod
    @raw_queries()
    def find_by_access_token(access_token, db):
        logger.debug('find_by_access_token')

        uuid = db.select_field('''
            SELECT main.get_user_uuid_by_access_token(%(access_token)s);
        ''', access_token=access_token)
        logger.debug(uuid)

        if not uuid:
            return None

        return User.find_by_user_uuid(uuid, 'all')

    @staticmethod
    def scope(scope):
        if scope == 'public_profile' or scope == 'public_all':
            return ', '.join(['uuid', 'name', 'avatar_url', 'status', 'visibility'])
        else:
            return '*'

    @staticmethod
    @raw_queries()
    def find_by_user_uuid(user_uuid, scope, db):
        logger.debug('find_by_user_uuid')

        user = db.select_record('''
            SELECT ''' + User.scope(scope) + ''' FROM main.get_user_by_uuid(%(user_uuid)s);
        ''', user_uuid=user_uuid)
        logger.debug(user)

        if not user['uuid']:
            return None

        return user

    @staticmethod
    @raw_queries()
    def drop_access_tokens(db):
        pass

    @staticmethod
    @raw_queries()
    def drop_refresh_tokens(db):
        pass

    @staticmethod
    @raw_queries()
    def get_all(limit, offset, scope, db):
        logger.debug('get_all')

        users = db.select_table('''
            SELECT id FROM main.get_users(%(limit)s, %(offset)s);
        ''', limit=limit, offset=offset)

        users_ids = [user['id'] for user in users]

        return User.get_all_by_ids(users_ids, scope)

    @staticmethod
    @raw_queries()
    def get_all_by_ids(users_ids, scope, db):
        logger.debug('get_all_by_ids')
        logger.debug(users_ids)

        users = db.select_table('''
            SELECT ''' + User.scope(scope) + ''' FROM main.get_users_by_ids(%(users_ids)s);
        ''', users_ids=users_ids)

        if scope == 'admin':
            for user in users:
                user['networks'] = UserNetwork.get_user_networks(user['id'])

        return users

    @staticmethod
    @raw_queries()
    def update_profile(user_id, visibility, status, db):
        logger.debug('update_profile')

        db.select_field('''
            SELECT main.update_user_profile(%(user_id)s, %(visibility)s, %(status)s);
        ''', user_id=user_id, visibility=visibility, status=status)

        return True
