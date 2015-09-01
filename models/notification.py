from decorators import *
from user import User
import json
from models.exceptions import ResourceIsNotFound

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Notification:
    @staticmethod
    @raw_queries()
    def get_notifications_by_user_id(user_id, limit, offset, db):
        notifications = db.select_table('''
            SELECT  id, type, data, user_id,
                    public.format_datetime(created_at) AS created_at
                FROM notifications.get_all(%(user_id)s, %(limit)s, %(offset)s);
        ''', user_id=user_id, limit=limit, offset=offset)

        result = []

        for record in notifications:
            data_for_result = {}
            data = record['data'] # already json in db

            # type with user
            if record['type'] in ['somebody_follows_me', 'somebody_sent_me_money']:
                try:
                    data_for_result['user'] = User.get_all_by_ids([record['user_id']], scope='public_profile')[0]
                    # for json.dumps:
                    data_for_result['user']['uuid'] = str(data_for_result['user']['uuid'])
                except Exception, e:
                    data_for_result['user'] = None

            # type with money
            if record['type'] == 'somebody_sent_me_money':
                try:
                    data_for_result['amount'] = data['amount']
                    data_for_result['currency'] = data['currency']
                except Exception, e:
                    data_for_result['amount'] = None
                    data_for_result['currency'] = None

            # remove user_id
            del record['user_id']

            # dump to json 'data_for_result'
            record['data'] = json.dumps(data_for_result)

        # that is all
        return notifications

    @staticmethod
    @raw_queries()
    def delete_notification(user_id, notification_id, db):
        result = db.select_field('''
            SELECT notifications.delete_notification(%(user_id)s, %(notification_id)s);
        ''', user_id=user_id, notification_id=notification_id)

        if not result:
            raise ResourceIsNotFound()

        return True


