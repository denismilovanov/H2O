from decorators import *
from models.invite import Invite
from models.user_network import UserNetwork
from models.user_session import UserSession
from models.user_account import UserAccount
from models.exceptions import InviteCodeAlreadyTakenException, InviteCodeDoesNotExistException, FacebookException, NotImplementedException, NotEnoughMoneyException
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
        need_to_download_avatar = None

        if not user_id:
            # new account
            invite = Invite.get_invite_code(invite_code, scope='all')
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
            # FUTURE: you may choose DB shard based on user_id and work with this user within his database
            # single transaction below:

            with db.t():
                user_id, user_uuid = UserNetwork.get_new_user_id()
                from models.generation import Generation
                num_in_generation = Generation.get_last_num_in_generation(generation)
                logger.info(str(generation) + ' ' + str(num_in_generation))

                db.select_field('''
                    SELECT main.upsert_user(
                        %(user_id)s, %(name)s, %(facebook_avatar_url)s, %(user_uuid)s,
                        %(network_id)s, %(user_network_id)s,
                        %(generation)s, %(num_in_generation)s
                    );
                ''',
                    user_id=user_id, user_uuid=user_uuid, name=user_data['name'], facebook_avatar_url=user_data['avatar_url'],
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

                # entrance gift
                if invite['entrance_gift']:
                    from models import Transaction
                    from H2O.settings import ENTRANCE_GIFT_AMOUNT, SYSTEM_CURRENCY
                    try:
                        Transaction.add_support(
                            invite['owner_id'],
                            user_id,
                            ENTRANCE_GIFT_AMOUNT,
                            SYSTEM_CURRENCY,
                            False # is_anonymous
                        )
                    except NotEnoughMoneyException:
                        # oh, ok
                        pass

            # newness flag
            is_new = True

            #
            user = User.get_by_id(user_id, scope='all_with_balance')
            need_to_download_avatar = user_data['avatar_url'] != None

        else:
            # need to take user['facebook_avatar_url'] before it will be changed by upsert
            user = User.get_by_id(user_id, scope='all_with_balance')
            need_to_download_avatar = user_data['avatar_url'] and \
                                      (user['facebook_avatar_url'] != user_data['avatar_url'] or
                                       not user['avatar_url'])

            # update information
            user_uuid = db.select_field('''
                SELECT main.upsert_user(%(user_id)s, %(name)s, %(facebook_avatar_url)s);
            ''', user_id=user_id, name=user_data['name'], facebook_avatar_url=user_data['avatar_url'])

        # after this we have 'user' variable

        # upsert network
        UserNetwork.upsert_network(user_id, network_id, user_network_id, access_token)

        # follow FB friend async
        if is_new:
            from tasks import ProcessFacebookFriendsTask
            ProcessFacebookFriendsTask(user['id'], access_token, 'follow_friends').enqueue()

        # download avatar if it is new or changed
        if need_to_download_avatar:
            import urllib, os
            from H2O.settings import AVATARS_DIR, AVATARS_URL

            # url and ext
            avatar_url = user_data['avatar_url']
            _, avatar_ext = os.path.splitext(avatar_url)

            #
            relative = '/' + str(user['uuid']) + avatar_ext[:avatar_ext.rfind('?')]
            our_avatar_path = AVATARS_DIR + relative
            our_avatar_url = AVATARS_URL + relative

            # download and save
            try:
                urllib.urlretrieve(avatar_url, our_avatar_path)

                db.select_field('''
                    SELECT main.set_user_avatar_url(%(user_id)s, %(our_avatar_url)s);
                ''', user_id=user_id, our_avatar_url=our_avatar_url)

                logger.info(our_avatar_url)
            except Exception, e:
                pass

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
            'balance': user['balance'],
            'hold': user['hold'],
            'free_invites_count': user['free_invites_count'],
            'follows_count': user['follows_count'],
        }, user_id

    @staticmethod
    def scope(scope):
        if scope in ['public_profile', 'my_personal_profile', 'public_profile_with_i_follow']:
            return ', '.join(['uuid', 'name', 'avatar_url', 'status', 'visibility', 'facebook_id', 'is_deleted',
                              'generation', 'num_in_generation', 'is_banned'])
        elif scope == 'my_personal_profile':
            return ', '.join(['uuid', 'name', 'avatar_url', 'status', 'visibility', 'facebook_id', 'is_deleted',
                              'generation', 'num_in_generation', 'is_banned', 'push_notifications'])
        elif scope == 'public_profile_with_id':
            return ', '.join(['id', 'uuid', 'name', 'avatar_url', 'status', 'visibility',
                              'facebook_id', 'is_deleted', 'is_banned'])
        elif scope == 'graph':
            return ', '.join(['uuid', 'name', 'generation', 'num_in_generation', 'is_deleted', 'is_banned', 'status'])
        else:
            return '*'

    @staticmethod
    @raw_queries()
    def get_user_by_uuid(user_uuid, scope, db):
        logger.info('get_user_by_uuid')

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
            user['free_invites_count'] = User.get_free_invites_count(me_id)

        if scope == 'all_with_balance':
            me_id = User.extract_user_id_from_uuid(user['uuid'])
            account = UserAccount.get_user_account(me_id)
            user['balance'] = float(account['balance'])
            user['hold'] = float(account['hold'])
            user['free_invites_count'] = User.get_free_invites_count(me_id)
            from models import UserFollow
            user['follows_count'] = UserFollow.get_user_follows_count(me_id)

        return user

    @staticmethod
    @raw_queries()
    def get_devices(user_id, db):
        return db.select_table('''
            SELECT * FROM main.get_user_devices(%(user_id)s);
        ''', user_id=user_id)

    @staticmethod
    @raw_queries()
    def get_free_invites_count(user_id, db):
        return db.select_field('''
            SELECT * FROM main.get_user_free_invites_count(%(user_id)s);
        ''', user_id=user_id)

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

        if scope == 'all_with_balance':
            from models import UserFollow
            for user in users:
                account = UserAccount.get_user_account(user['id'])
                user['balance'] = float(account['balance'])
                user['hold'] = float(account['hold'])
                user['free_invites_count'] = User.get_free_invites_count(user['id'])
                user['follows_count'] = UserFollow.get_user_follows_count(user['id'])

        if scope == 'public_profile_with_i_follow':
            from models import UserFollow
            for user in users:
                user_id = User.extract_user_id_from_uuid(user['uuid'])
                user['i_follow'] = UserFollow.does_user_follow_user(viewer_id, user_id)
                user['follows_count'] = UserFollow.get_user_follows_count(user_id)

        return users

    @staticmethod
    def get_by_id(user_id, scope):
        users = User.get_all_by_ids([user_id], scope)
        try:
            return users[0]
        except:
            return None

    @staticmethod
    @raw_queries()
    def get_user_id_by_num_in_generation(generation, num_in_generation, db):
        logger.info('get_user_id_by_num_in_generation')

        return db.select_field('''
            SELECT main.get_user_id_by_num_in_generation(%(generation)s, %(num_in_generation)s);
        ''', generation=generation, num_in_generation=num_in_generation)

    @staticmethod
    @raw_queries()
    def update_profile(user_id, visibility, status, push_notifications, is_deleted, db):
        logger.info('update_profile')

        db.select_field('''
            SELECT main.update_user_profile(%(user_id)s, %(visibility)s, %(status)s, %(push_notifications)s);
        ''', user_id=user_id, visibility=visibility, status=status, push_notifications=push_notifications)

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

    @staticmethod
    @raw_queries()
    def get_zero_generation(type, db):
        from H2O.settings import DEBUG
        first_generation_users = db.select_table('''
            SELECT main.get_users_ids_by_generation(0, %(debug)s) AS user_id;
        ''', debug=DEBUG)

        zero_generation_users_ids = [first_generation_user['user_id'] for first_generation_user in first_generation_users]

        users = User.get_all_by_ids(zero_generation_users_ids, scope='graph')

        if type == 'extended':
            from models import UserFollow
            for user in users:
                user_id = User.extract_user_id_from_uuid(user['uuid'])
                user['follows'] = User.get_all_by_ids(UserFollow.get_user_follows_ids(user_id), scope='graph')

        return users

