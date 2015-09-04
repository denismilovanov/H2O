from decorators import *
from exceptions import UserIsAlreadyFollowed, UserIsNotFound
from models import User

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class UserFollow:
    @staticmethod
    @raw_queries()
    def upsert_user_follow(user_id, follow_user_uuid, db):
        follow_user = User.find_by_user_uuid(follow_user_uuid, scope='all')

        if not follow_user: # or follow_user['is_deleted']:
            raise UserIsNotFound()

        if follow_user['id'] == user_id:
            raise UserIsAlreadyFollowed()

        result = db.select_field('''
            SELECT main.upsert_user_follow(%(user_id)s, %(follow_user_id)s);
        ''', user_id=user_id, follow_user_id=follow_user['id'])

        if not result:
            raise UserIsAlreadyFollowed()

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
    @raw_queries()
    def delete_user_follow(user_id, follow_user_uuid, db):
        follow_user = User.find_by_user_uuid(follow_user_uuid, scope='all')

        if not follow_user:
            raise UserIsNotFound()

        result = db.select_field('''
            SELECT main.delete_user_follow(%(user_id)s, %(follow_user_id)s);
        ''', user_id=user_id, follow_user_id=follow_user['id'])

        if not result:
            raise UserIsNotFound()

    @staticmethod
    @raw_queries()
    def get_user_follows(user_id, limit, offset, search_query, db):
        users = db.select_table('''
            SELECT main.get_user_follows_ids(%(user_id)s, %(limit)s, %(offset)s) AS follow_user_id;
        ''', user_id=user_id, limit=limit, offset=offset)

        users_ids = [u['follow_user_id'] for u in users]

        return User.get_all_by_ids(users_ids, scope='public_profile')

    @staticmethod
    @raw_queries()
    def get_user_follows_ids(user_id, db):
        users = db.select_table('''
            SELECT main.get_user_follows_ids(%(user_id)s, 100000, 0) AS follow_user_id;
        ''', user_id=user_id)

        return [u['follow_user_id'] for u in users]
