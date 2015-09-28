from decorators import *
from user import User
import json
from models.exceptions import ResourceIsNotFoundException
from models import UserFollow

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Notification:
    @staticmethod
    def process_notification(record, user_id):
        data_for_result = {}
        data = record['data'] # already json in db

        # type with user
        if record['type'] in ['somebody_follows_me', 'somebody_sent_me_money']:
            try:
                data_for_result['user'] = User.get_by_id(record['counter_user_id'], scope='public_profile')
                # for json.dumps:
                data_for_result['user']['uuid'] = str(data_for_result['user']['uuid'])
            except Exception, e:
                data_for_result['user'] = None

        # type with money
        if record['type'] == 'somebody_sent_me_money':
            data_for_result['amount'] = data.get('amount', 0)
            data_for_result['currency'] = data.get('currency', 'usd')
            is_anonymous = data.get('is_anonymous', True)

            if is_anonymous:
                data_for_result['user'] = None

        # type with notification_count
        if record['type'] == 'new_invites_available':
            try:
                data_for_result['invites_count'] = data['invites_count']
            except Exception, e:
                data_for_result['invites_count'] = 0

        # type with user again
        if record['type'] in ['somebody_follows_me', 'somebody_sent_me_money']:
            # do I follow this user?
            if data_for_result['user']:
                data_for_result['user']['i_follow'] = UserFollow.does_user_follow_user(user_id, record['counter_user_id'])

        # remove counter_user_id
        del record['counter_user_id']

        #
        record['data'] = data_for_result

    @staticmethod
    @raw_queries()
    def get_notifications_by_user_id(user_id, limit, offset, db):
        notifications = db.select_table('''
            SELECT  id, type, data, counter_user_id,
                    public.format_datetime(created_at) AS created_at
                FROM notifications.get_all(%(user_id)s, %(limit)s, %(offset)s);
        ''', user_id=user_id, limit=limit, offset=offset)

        result = []

        for record in notifications:
            Notification.process_notification(record, user_id)

        # that is all
        return notifications

    @staticmethod
    @raw_queries()
    def delete_notification(user_id, notification_id, db):
        result = db.select_field('''
            SELECT notifications.delete_notification(%(user_id)s, %(notification_id)s);
        ''', user_id=user_id, notification_id=notification_id)

        if not result:
            raise ResourceIsNotFoundException()

        return True

    @staticmethod
    @raw_queries()
    def delete_all_notifications_by_user_id(user_id, db):
        db.select_field('''
            SELECT notifications.delete_all_notifications_by_user_id(%(user_id)s);
        ''', user_id=user_id)

    @staticmethod
    @raw_queries()
    def add_notification(user_id, notification_type, data, counter_user_id, db):
        return db.select_field('''
            SELECT notifications.add_notification(%(user_id)s, %(notification_type)s, %(data)s, %(counter_user_id)s);
        ''',
            user_id=user_id, notification_type=notification_type,
            data=json.dumps(data), counter_user_id=counter_user_id
        )

    @staticmethod
    @raw_queries()
    def get_notification_for_push(user_id, notification_id, db):
        notification = db.select_record('''
            SELECT  id, type, data, counter_user_id,
                    public.format_datetime(created_at) AS created_at
                FROM notifications.get_notification(%(user_id)s, %(notification_id)s);
        ''', user_id=user_id, notification_id=notification_id)

        Notification.process_notification(notification, user_id)

        # make push header, see pusher.py
        header = None
        if notification['type'] == 'somebody_follows_me':
            header = 'You have a new follower'
        elif notification['type'] == 'somebody_sent_me_money':
            header = 'You have been supported'
        elif notification['type'] == 'new_invites_available':
            header = 'New invites are available for you'

        notification['push_header'] = header

        #
        return notification


