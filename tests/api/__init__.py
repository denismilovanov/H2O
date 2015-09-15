'''
Usage:
    ./manage.py test tests.api
'''
from test_session import SessionTestCase
from test_profile import ProfileTestCase
from test_invite_codes import InviteCodesTestCase
from test_follows import FollowsTestCase
from test_transactions import TransactionsTestCase
from test_statistics import StatisticsTestCase
from test_notifications import NotificationsTestCase
from test_session_create_new_user import SessionCreateNewUserTestCase
from test_graph import GraphTestCase
from test_deposits import DepositsTestCase
from test_error import ErrorTestCase
