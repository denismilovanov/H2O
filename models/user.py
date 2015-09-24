from decorators import *
from models.invite import Invite
from models.user_network import UserNetwork
from models.user_session import UserSession
from models.user_account import UserAccount
from models.exceptions import InviteCodeAlreadyTakenException, InviteCodeDoesNotExistException, FacebookException, NotImplementedException
from models.facebook_wrapper import FacebookWrapper

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class User:
    @staticmethod
    def extract_user_id_from_uuid(uuid):
        uuid = str(uuid)
        id = uuid[:8]
        id = int(id, 16)

        # test cases
        if 0 < id < 100000:
            id *= -1

        return id

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

            #
            invite_owner = User.get_by_id(invite['owner_id'], scope='all')
            logger.info(invite_owner)

            #
            generation = invite_owner['generation'] + 1

            # create
            user_id, user_uuid = UserNetwork.get_new_user_id()
            from models.graph import Graph
            num_in_generation = Graph.get_last_num_in_generation(generation)
            logger.info(str(generation) + ' ' + str(num_in_generation))

            # FUTURE: you may choose DB shard based on user_id and work with this user within his database
            # single transaction below:
            with db.t():
                db.select_field('''
                    SELECT main.upsert_user(
                        %(user_id)s, %(name)s, %(avatar_url)s, %(user_uuid)s,
                        %(network_id)s, %(user_network_id)s,
                        %(generation)s, %(num_in_generation)s
                    );
                ''',
                    user_id=user_id, user_uuid=user_uuid, name=user_data['name'], avatar_url=user_data['avatar_url'],
                    network_id=network_id, user_network_id=user_network_id,
                    generation=generation, num_in_generation=num_in_generation
                )
                logger.info(user_uuid)

                # use code
                Invite.use_invite_code(user_id, invite_code, db)

                # create codes
                from H2O.settings import INVITES_COUNT_FOR_NEW_USER
                Invite.create_invite_codes_for_user_id(user_id, INVITES_COUNT_FOR_NEW_USER, db)

                # stat for user
                from models.statistics import Statistics
                Statistics.create_user_records(user_id, db)

                # account
                from user_account import UserAccount
                UserAccount.create_user_accounts(user_id, db)

            # follow facebook friends
            from models import UserFollow
            UserFollow.follow_my_facebook_fiends_by_their_ids(user_id, user_data.get('facebook_friends_ids', []))

            # newness flag
            is_new = True

        else:
            # update information
            user_uuid = db.select_field('''
                SELECT main.upsert_user(%(user_id)s, %(name)s, %(avatar_url)s);
            ''', user_id=user_id, name=user_data['name'], avatar_url=user_data['avatar_url'])

        # for is_deleted and generation in response
        user = User.find_by_user_uuid(user_uuid, scope='all')

        # upsert network
        UserNetwork.upsert_network(user_id, network_id, user_network_id, access_token)

        # that was all
        return {
            'uuid': user_uuid,
            'is_new': is_new,
            'avatar_url': user_data['avatar_url'],
            'name': user_data['name'],
            'is_deleted': user['is_deleted'],
            'is_banned': user['is_banned'],
            'generation': user['generation'],
            'num_in_generation': user['num_in_generation'],
        }, user_id

    @staticmethod
    def scope(scope):
        if scope in ['public_profile', 'my_personal_profile', 'public_profile_with_i_follow']:
            return ', '.join(['uuid', 'name', 'avatar_url', 'status', 'visibility', 'facebook_id', 'is_deleted',
                              'generation', 'num_in_generation'])
        elif scope == 'public_profile_with_id':
            return ', '.join(['id', 'uuid', 'name', 'avatar_url', 'status', 'visibility', 'facebook_id', 'is_deleted'])
        elif scope == 'graph':
            return ', '.join(['uuid', 'name', 'generation', 'num_in_generation', 'is_deleted', 'status'])
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

        if scope == 'my_personal_profile':
            me_id = User.extract_user_id_from_uuid(user['uuid'])
            user['balance'] = float(UserAccount.get_user_account(me_id)['balance'])
            user['push_notifications'] = True # UserSettings.get_user_settings(me_id)['push_notifications']

        return user

    @staticmethod
    @raw_queries()
    def get_devices(user_id, db):
        return db.select_table('''
            SELECT * FROM main.get_user_devices(%(user_id)s);
        ''', user_id=user_id)

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
    def get_all_by_ids(users_ids, scope, db, viewer_id=None):
        logger.info('get_all_by_ids')
        logger.info(users_ids)

        users = db.select_table('''
            SELECT ''' + User.scope(scope) + ''' FROM main.get_users_by_ids(%(users_ids)s);
        ''', users_ids=users_ids)

        if scope == 'admin':
            for user in users:
                user['networks'] = UserNetwork.get_user_networks(user['id'])

        if scope == 'graph':
            for user in users:
                user['follows'] = []
                user['followed_by'] = []

        if scope == 'all_with_balance':
            for user in users:
                account = UserAccount.get_user_account(user['id'])
                user['balance'] = float(account['balance'])
                user['hold'] = float(account['hold'])

        if scope == 'public_profile_with_i_follow':
            from models import UserFollow
            for user in users:
                user['i_follow'] = UserFollow.does_user_follow_user(
                    viewer_id, User.extract_user_id_from_uuid(user['uuid'])
                )

        return users

    @staticmethod
    def get_by_id(user_id, scope):
        logger.info('get_by_id')
        logger.info(user_id)

        users = User.get_all_by_ids([user_id], scope)
        try:
            return users[0]
        except:
            return None

    @staticmethod
    @raw_queries()
    def get_user_id_by_num_in_generation(generation, num_in_generation, db):
        return db.select_field('''
            SELECT main.get_user_id_by_num_in_generation(%(generation)s, %(num_in_generation)s);
        ''', generation=generation, num_in_generation=num_in_generation)

    @staticmethod
    @raw_queries()
    def update_profile(user_id, visibility, status, push_notifications, is_deleted, db):
        logger.info('update_profile')

        db.select_field('''
            SELECT main.update_user_profile(%(user_id)s, %(visibility)s, %(status)s);
        ''', user_id=user_id, visibility=visibility, status=status)

        if not is_deleted:
            User.undelete_profile(user_id)

        return True

    @staticmethod
    @raw_queries()
    def delete_profile(user_id, db):
        logger.info('delete_profile')

        db.select_field('''
            SELECT main.delete_user_profile(%(user_id)s);
        ''', user_id=user_id)

        return True

    @staticmethod
    @raw_queries()
    def undelete_profile(user_id, db):
        logger.info('undelete_profile')

        db.select_field('''
            SELECT main.undelete_user_profile(%(user_id)s);
        ''', user_id=user_id)

        return True
