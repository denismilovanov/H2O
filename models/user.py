from decorators import *
from models.invite import Invite
from models.user_network import UserNetwork
from models.user_session import UserSession
from models.exceptions import InviteCodeAlreadyTakenException, InviteCodeDoesNotExistException, FacebookException, NotImplementedException
from models.facebook_wrapper import FacebookWrapper

import logging
logging.basicConfig(level=logging.INFO)
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
        logger.info('upsert')
        logger.info(user_data)

        user_network_id = user_data['id']

        # search
        user_id = UserNetwork.find_user_by_network(network_id, user_network_id)

        is_new = False

        if not user_id:
            # new account
            invite = Invite.get_invite_code(invite_code)
            logger.info(invite)

            if not invite:
                # there is no code
                raise InviteCodeDoesNotExistException

            if invite['is_used']:
                # invite is used
                raise InviteCodeAlreadyTakenException

            # create
            user_id, user_uuid = UserNetwork.get_new_user_id()

            # choose DB based on user_id:
            db.select_field('''
                SELECT main.upsert_user(%(user_id)s, %(name)s, %(avatar_url)s, %(user_uuid)s);
            ''', user_id=user_id, user_uuid=user_uuid, name=user_data['name'], avatar_url=user_data['avatar_url'])
            logger.info(user_uuid)

            # use code
            Invite.use_invite_code(invite_code, user_id)

            # create codes
            Invite.create_invite_codes_for_user_id(user_id, 3)

            # newness flag
            is_new = True

        else:
            # update information
            user_uuid = db.select_field('''
                SELECT main.upsert_user(%(user_id)s, %(name)s, %(avatar_url)s);
            ''', user_id=user_id, name=user_data['name'], avatar_url=user_data['avatar_url'])

        # upsert network
        UserNetwork.upsert_network(user_id, network_id, user_network_id, access_token)

        # that was all
        return {
            'uuid': user_uuid,
            'is_new': is_new,
            'avatar_url': user_data['avatar_url'],
            'name': user_data['name'],
        }, user_id

    @staticmethod
    def scope(scope):
        if scope == 'public_profile':
            return ', '.join(['uuid', 'name', 'avatar_url', 'status', 'visibility'])
        else:
            return '*'

    @staticmethod
    @raw_queries()
    def find_by_user_uuid(user_uuid, scope, db):
        logger.info('find_by_user_uuid')

        # user_uuid contains user_id
        # user_id maps to database
        user = db.select_record('''
            SELECT ''' + User.scope(scope) + ''' FROM main.get_user_by_uuid(%(user_uuid)s);
        ''', user_uuid=user_uuid)
        logger.info(user)

        if not user['uuid']:
            return None

        return user

    @staticmethod
    @raw_queries()
    def get_all(limit, offset, scope, db):
        logger.info('get_all')

        users = db.select_table('''
            SELECT id FROM main.get_users(%(limit)s, %(offset)s);
        ''', limit=limit, offset=offset)

        users_ids = [user['id'] for user in users]

        return User.get_all_by_ids(users_ids, scope)

    @staticmethod
    @raw_queries()
    def get_all_by_ids(users_ids, scope, db):
        logger.info('get_all_by_ids')
        logger.info(users_ids)

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
        logger.info('update_profile')

        db.select_field('''
            SELECT main.update_user_profile(%(user_id)s, %(visibility)s, %(status)s);
        ''', user_id=user_id, visibility=visibility, status=status)

        return True

    @staticmethod
    @raw_queries()
    def delete_profile(user_id, db):
        logger.info('delete_profile')

        db.select_field('''
            SELECT main.delete_user_profile(%(user_id)s);
        ''', user_id=user_id)

        return True
