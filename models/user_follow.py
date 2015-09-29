from decorators import *
from exceptions import UserIsAlreadyFollowedException, UserIsNotFoundException
from models import User

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class UserFollow:
    @staticmethod
    @raw_queries()
    def upsert_user_follow(user_id, follow_user_uuid, db):
        logger.info('upsert_user_follow ' + str(user_id) + ' ' + str(follow_user_uuid))
        follow_user = User.get_user_by_uuid(follow_user_uuid, scope='all')

        if not follow_user: # or follow_user['is_deleted']:
            raise UserIsNotFoundException()

        if follow_user['id'] == user_id:
            raise UserIsAlreadyFollowedException()

        # insert into follows and followed_by
        with db.t():
            result = db.select_field('''
                SELECT main.upsert_user_follow(%(user_id)s, %(follow_user_id)s);
            ''', user_id=user_id, follow_user_id=follow_user['id'])

            # check
            if not result:
                raise UserIsAlreadyFollowedException()

            db.select_field('''
                SELECT main.upsert_user_followed_by(%(follow_user_id)s, %(user_id)s);
            ''', user_id=user_id, follow_user_id=follow_user['id'])

        # send notification
        # sending though queue
        try:
            from tasks.notify_follow_task import NotifyFollowTask
            # follow_user['id'] will receive notification
            # user_id will become counter_user_id inside NotifySupportTask
            NotifyFollowTask(follow_user['id'], user_id).enqueue()
        except Exception, e:
            # there is no need to raise exception and scare user
            logger.info(e)

        return True

    @staticmethod
    def follow_my_facebook_fiends_by_their_ids(user_id, facebook_friends_ids):
        logger.info('follow_my_facebook_fiends_by_their_ids')
        logger.info(facebook_friends_ids)

        # map facebook ids to our ids
        from models import UserNetwork
        facebook_friends_our_ids = UserNetwork.find_users_by_network(1, facebook_friends_ids)

        # iterate
        for facebook_friend_our_id in facebook_friends_our_ids:
            # get uuid
            facebook_friend_in_our_system = User.get_by_id(facebook_friend_our_id, scope='all')
            # follow
            if facebook_friend_in_our_system:
                UserFollow.upsert_user_follow(user_id, facebook_friend_in_our_system['uuid'])

    @staticmethod
    @raw_queries()
    def delete_user_follow(user_id, follow_user_uuid, db):
        follow_user = User.get_user_by_uuid(follow_user_uuid, scope='all')

        if not follow_user:
            raise UserIsNotFoundException()

        with db.t():
            result = db.select_field('''
                SELECT main.delete_user_follow(%(user_id)s, %(follow_user_id)s);
            ''', user_id=user_id, follow_user_id=follow_user['id'])

            if not result:
                raise UserIsNotFoundException()

            db.select_field('''
                SELECT main.delete_user_followed_by(%(follow_user_id)s, %(user_id)s);
            ''', user_id=user_id, follow_user_id=follow_user['id'])

    @staticmethod
    @raw_queries()
    def get_user_follows(user_id, limit, offset, search_query, db):
        users = db.select_table('''
            SELECT main.get_user_follows_ids(%(user_id)s, %(limit)s, %(offset)s, %(search_query)s) AS follow_user_id;
        ''', user_id=user_id, limit=limit, offset=offset, search_query=search_query)

        users_ids = [u['follow_user_id'] for u in users]

        return User.get_all_by_ids(users_ids, scope='public_profile')

    @staticmethod
    @raw_queries()
    def get_user_follows_ids(user_id, db):
        users = db.select_table('''
            SELECT main.get_user_follows_ids(%(user_id)s, 100000, 0) AS follow_user_id;
        ''', user_id=user_id)

        return [u['follow_user_id'] for u in users]

    @staticmethod
    @raw_queries()
    def does_user_follow_user(user_id, follow_user_id, db):
        follow = db.select_table('''
            SELECT * FROM main.get_user_follow(%(user_id)s, %(follow_user_id)s);
        ''', user_id=user_id, follow_user_id=follow_user_id)

        return len(follow) > 0 and follow[0]['user_id'] != None

    @staticmethod
    @raw_queries()
    def get_user_follows_count(user_id, db):
        return db.select_field('''
            SELECT main.get_user_follows_count(%(user_id)s);
        ''', user_id=user_id)

    @staticmethod
    @raw_queries()
    def get_user_followed_by_ids(user_id, db):
        users = db.select_table('''
            SELECT main.get_user_followed_by_ids(%(user_id)s, 100000, 0) AS followed_by_user_id;
        ''', user_id=user_id)

        return [u['followed_by_user_id'] for u in users]
