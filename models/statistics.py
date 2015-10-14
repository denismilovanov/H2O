from decorators import *
from models import User, UserFollow

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Statistics:
    @staticmethod
    @raw_queries()
    def get_statistics_overall(user_id, db):
        statistics = db.select_table('''
            SELECT transaction_direction, transactions_count, users_count, transactions_amount_sum
                FROM statistics.get_statistics_overall(%(user_id)s);
        ''', user_id=user_id)

        result = {}

        for record in statistics:
            result[str(record['transaction_direction']) + 's'] = {
                'transactions_count': record['transactions_count'],
                'transactions_amount_sum': record['transactions_amount_sum'],
                'users_count': record['users_count'],
                'users': Statistics.get_statistics_counter_users_inner(user_id, record['transaction_direction'], 5, 0, db)
            }

        return result

    @staticmethod
    @raw_queries()
    def get_statistics_counter_users(user_id, transaction_direction, limit, offset, db):
        return Statistics.get_statistics_counter_users_inner(user_id, transaction_direction, limit, offset, db)

    @staticmethod
    def get_statistics_counter_users_inner(user_id, transaction_direction, limit, offset, db):
        # get stat
        statistics = db.select_table('''
            SELECT *
                FROM statistics.get_statistics_counter_users(%(user_id)s, %(transaction_direction)s, %(limit)s, %(offset)s);
        ''', user_id=user_id, transaction_direction=transaction_direction, limit=limit, offset=offset)

        # build hash from transactons_*
        transactions_counts = dict([(record['counter_user_id'], record['transactions_count']) for record in statistics])
        transactions_amounts_sums = dict([(record['counter_user_id'], record['transactions_amount_sum']) for record in statistics])

        # collect users ids
        users_ids = [record['counter_user_id'] for record in statistics]

        # get all users
        users = User.get_all_by_ids(users_ids, scope='public_profile_with_i_follow', viewer_id=user_id)

        # add transactions_count to user
        for user in users:
            user['id'] = User.extract_user_id_from_uuid(user['uuid'])
            user['transactions_count'] = transactions_counts[user['id']]
            user['transactions_amount_sum'] = transactions_amounts_sums[user['id']]
            user['follows_count'] = UserFollow.get_user_follows_count(user['id'])
            del user['id']

        # order by sum
        users = sorted(users, key=lambda k: k['transactions_amount_sum'], reverse=True)

        #
        return users

    @staticmethod
    def create_user_records(user_id, db):
        db.select_field('''
            SELECT statistics.create_user_records(%(user_id)s);
        ''', user_id=user_id)

        return True

    @staticmethod
    @raw_queries()
    def update_statistics_via_transaction(user_id, transaction_id, db):
        # get transactions
        from models.transaction import Transaction
        transaction = Transaction.get_transaction_by_id(user_id, transaction_id)

        # skip
        if not transaction:
            return True
        if transaction['status'] != 'success':
            return True
        if transaction['direction'] not in ['support', 'receive']:
            return True

        # do update
        db.select_field('''
            SELECT statistics.update_statistics_via_transaction(
                %(user_id)s, %(counter_user_id)s, %(direction)s,
                %(amount)s, %(currency)s, %(is_anonymous)s
            );
        ''',
            user_id=user_id,
            counter_user_id=transaction['counter_user_id'],
            direction=transaction['direction'],
            amount=transaction['amount'],
            currency=transaction['currency'],
            is_anonymous=transaction['is_anonymous']
        )

        return True

