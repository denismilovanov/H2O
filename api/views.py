from rest_framework.decorators import api_view
from views_helpers import created, bad_request, unavailable, forbidden, unauthorized, conflict
from views_helpers import ok, ok_raw, internal_server_error, not_found, not_acceptable, no_content
from models import *
from models.exceptions import *
import datetime

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_boolean(smth):
    return smth in [True, 'true', '1', 1]

#
def get_limit_and_offset(request):
    limit = request.GET.get('limit', None)
    offset = request.GET.get('offset', None)

    if limit:
        limit = int(limit)
    if offset:
        offset = int(offset)

    if not limit:
        limit = int(request.data.get('limit', 20))
    if not offset:
        offset = int(request.data.get('offset', 0))

    if limit < 0:
        limit = 20
    if offset < 0:
        offset = 0

    if limit > 100:
        limit = 100

    return limit, offset
    # raise Exception()

# decorator for all methods
def authorization_needed(func):
    def inner(*k, **v):
        request = k[0]
        refresh_token = request.data.get('refresh_token')
        access_token = None
        user = {}

        if  not refresh_token and \
            not (request.path.startswith('/v1/session') and request.method == 'POST'):

            logger.info('Need to authorize')

            # get token
            try:
                access_token = request.META.get('HTTP_ACCESS_TOKEN')
                if not access_token:
                    headers = request.META.get('headers')
                    if headers:
                        access_token = headers.get('Access-Token')

                logger.info('access token ' + str(access_token))

                if not access_token:
                    raise AccessTokenDoesNotExist()

            except Exception, e:
                return unauthorized(e)
        else:
            logger.info('No need to authorize')

        # need to authorize with this token
        if access_token:
            # get user
            try:
                uuid = UserSession.get_user_uuid_by_access_token(access_token)

                user = None
                if uuid:
                    user = User.find_by_user_uuid(uuid, 'all')

                if not user:
                    raise AccessTokenDoesNotExist()

            except AccessTokenDoesNotExist, e:
                return unauthorized(e)
            except Exception, e:
                return internal_server_error(e)

        # pass user
        user['access_token'] = access_token
        v['user'] = user

        # call decorated function
        try:
            return func(*k, **v)
        except Exception, e:
            return internal_server_error(e)

    return inner

# error
@api_view(['GET', 'POST', 'PATCH', 'PUT', 'DELETE'])
@authorization_needed
def error(request, http_code, user):
    #http_code = request.data.get('http_code')
    #if not http_code:
    #    http_code = request.GET.get('http_code')

    http_code = int(http_code)

    # error description
    error = ''
    try:
       error = {
            400: 'BAD_REQUEST',
            401: 'UNAUTHORIZED',
            403: 'FORBIDDEN',
            404: 'RESOURSE_IS_NOT_FOUND',
            406: 'EMAIL_IS_ALREADY_USED',
            500: 'INTERNAL_SERVER_ERROR',
            503: 'UNAVAILABLE',
        }[http_code]
    except:
        pass

    data = {
        'error': error,
    }

    logger.info('METHOD: error ' + str(http_code) + ' ' + str(error))

    # response
    from views_helpers import JSONResponse
    return JSONResponse(data, status=http_code)

# params
@api_view(['GET'])
@authorization_needed
def params(request, user):
    logger.info('METHOD: params')

    params = {
        'providers': {
            'paypal': {
                'commissions': {
                    'deposit': {
                        'percent': 2.9,
                        'flat': 0.30,
                    },
                    'withdrawal': {
                        'percent': 1.5,
                        'flat': 0.30,
                    },
                },
            },
        },
    }

    return ok_raw(params)

# session
@api_view(['POST', 'PATCH', 'DELETE'])
@authorization_needed
def session(request, user):
    logger.info('METHOD: session')

    # new session
    if request.method == 'POST':
        #input
        try:
            network_id = request.data['network_id']
            access_token = request.data['access_token']
            invite_code = request.data.get('invite_code')
            device_type = request.data['device_type']
            push_token = request.data.get('push_token')
            logger.info(request.data)

        except Exception, e:
            return bad_request(BadRequest(e))

        # connecting to facebook
        try:
            user_data = User.get_user_via_network(network_id, access_token)
        except FacebookException, e:
            return unavailable(e)
        except Exception, e:
            return forbidden(e)

        # creating or getting user
        try:
            user, user_id = User.upsert(user_data, network_id, access_token, invite_code)
        except (InviteCodeAlreadyTakenException, InviteCodeDoesNotExistException), e:
            return forbidden(e)
        except Exception, e:
            return internal_server_error(e)

        # creating session
        try:
            session = UserSession.upsert_user_session(user_id, device_type, push_token)
        except Exception, e:
            return internal_server_error(e)

        # result
        return created(user=user, session=session)

    # refresh session
    elif request.method == 'PATCH':
        refresh_token = request.data.get('refresh_token')
        push_token = request.data.get('push_token')

        if not refresh_token and not push_token:
            return bad_request(BadRequest())

        if refresh_token:
            access_token, access_token_expires_at = UserSession.refresh_access_token(refresh_token)

            if not access_token:
                return unauthorized(ResfreshTokenDoesNotExist())

            from H2O.settings import ACCESS_TOKEN_EXPIRES_IN
            return ok(
                access_token=access_token,
                access_token_expires_in=ACCESS_TOKEN_EXPIRES_IN,
                access_token_expires_at=access_token_expires_at
            )

        if push_token:
            UserDevice.upsert_push_token(user['id'], push_token)

            return no_content()

    # logout
    elif request.method == 'DELETE':
        UserSession.delete_session(user['id'], user['access_token'])

        return no_content()

# profile
@api_view(['GET'])
@authorization_needed
def user(request, user_uuid, user):
    logger.info('METHOD: user')

    me = False

    if user_uuid == 'me':
        user_uuid = user['uuid']
        me = True

    if not me:
        # user I want to view profile
        user_to_view = User.find_by_user_uuid(user_uuid, scope='public_profile')
        if not user_to_view:
            return not_found(UserIsNotFound())

        # get all data to check if I follow this user
        user_to_view_all_data = User.find_by_user_uuid(user_uuid, scope='all')
        # do I follow this user?
        user_to_view['i_follow'] = UserFollow.does_user_follow_user(user['id'], user_to_view_all_data['id'])

    else:
        # this is me
        user_to_view = User.find_by_user_uuid(user_uuid, scope='my_personal_profile')

    return ok_raw(user_to_view)

# list of user
@api_view(['GET'])
@authorization_needed
def users(request, user):
    logger.info('METHOD: users')

    users = User.get_all(1000, 0, scope='public_profile')

    return ok_raw(users)

# profile
@api_view(['PATCH', 'DELETE'])
@authorization_needed
def profile(request, user):
    logger.info('METHOD: profile')

    if request.method == 'PATCH':
        #input
        try:
            visibility = request.data.get('visibility')
            status = request.data.get('status')
            push_notifications = get_boolean(request.data.get('push_notifications', True))
            is_deleted = get_boolean(request.data.get('is_deleted'))
            logger.info(request.data)

        except Exception, e:
            return bad_request(BadRequest(e))

        User.update_profile(user['id'], visibility, status, push_notifications, is_deleted)

    elif request.method == 'DELETE':
        User.delete_profile(user['id'])

    return no_content()

# invite codes list
@api_view(['GET'])
@authorization_needed
def invite_codes(request, user):
    logger.info('METHOD: invite_codes')

    return ok_raw(Invite.get_invite_codes_by_user_id(user['id'], scope='public_invite_codes'))


# update invite code
@api_view(['PATCH'])
@authorization_needed
def invite_code(request, invite_code, user):
    logger.info('METHOD: invite_code')

    #input
    try:
        email = request.data['email']
        entrance_gift = get_boolean(request.data.get('entrance_gift', False))
    except Exception, e:
        return bad_request(BadRequest(e), email)

    # get code
    code = Invite.get_invite_code(invite_code)
    logger.info(code)

    if not code or code['status'] != 'free':
        # there is no code available
        return not_found(InviteCodeDoesNotExistException(), email)

    if code['owner_id'] != user['id']:
        # code is not mine
        return forbidden(InviteCodeDoesNotExistException(), email)

    # making invite
    try:
        Invite.invite_user_via_invite_code_and_email(user['id'], invite_code, email, entrance_gift)
    except InvalidEmail, e:
        return bad_request(e, email)
    except EmailIsAlreadyUsed, e:
        return not_acceptable(e, email)
    except YouHaveInvitedThisEmail, e:
        return not_acceptable(e, email)

    return ok(email=email)

# add, get, or delete follow
@api_view(['GET', 'POST', 'DELETE'])
@authorization_needed
def follow(request, user_uuid, user):
    logger.info('METHOD: follow')

    if request.method == 'POST':
        try:
            UserFollow.upsert_user_follow(user['id'], user_uuid)
        except UserIsAlreadyFollowed, e:
            return not_acceptable(e)
        except UserIsNotFound, e:
            return not_found(UserIsNotFound())

        return created()

    elif request.method == 'DELETE':
        try:
            UserFollow.delete_user_follow(user['id'], user_uuid)
        except UserIsNotFound, e:
            return not_found(UserIsNotFound())

        return no_content()

    else:
        return follows_inner(request, user_uuid, user)

# list of follows
@api_view(['GET'])
@authorization_needed
def follows(request, user_uuid, user):
    return follows_inner(request, user_uuid, user)

# for 2 previous
def follows_inner(request, user_uuid, user):
    logger.info('METHOD: follows')

    #input
    try:
        limit, offset = get_limit_and_offset(request)
        search_query = request.GET.get('search_query')
    except Exception, e:
        return bad_request(BadRequest(e))

    # look at the user to get follows list about
    if user_uuid == 'my':
        user_id = user['id']
    else:
        user_by_uuid = User.find_by_user_uuid(user_uuid, scope='all')
        if not user_by_uuid:
            return not_found(UserIsNotFound())

        user_id = user_by_uuid['id']

    # get list
    follows = UserFollow.get_user_follows(user_id, limit, offset, search_query)

    # if we need to get list of other user's follows
    # then we shall calculate i_follow
    if user['id'] != user_id:
        my_follows = UserFollow.get_user_follows(user['id'], int(1e6), 0, None)

        my_follows_uuids = [my_follow['uuid'] for my_follow in my_follows]

        for follow in follows:
            follow['i_follow'] = follow['uuid'] in my_follows_uuids
    else:
        for follow in follows:
            follow['i_follow'] = True

    # that's all
    return ok_raw(follows)

def get_from_date_to_date(request):
    try:
        from_date = request.GET['from_date']
        to_date = request.GET['to_date']
    except Exception, e:
        raise BadRequest(e)

    # special dates
    if from_date == 'now':
        from_date = str(datetime.datetime.now().date())
    if to_date == 'now':
        to_date = str(datetime.datetime.now().date())

    # parse string repr
    try:
        from dateutil.parser import parse
        from_date = parse(from_date)
        to_date = parse(to_date)
    except Exception, e:
        raise BadRequest(e)

    return from_date, to_date


# supports
@api_view(['GET'])
@authorization_needed
def supports(request, whose, user):
    logger.info('METHOD: supports')

    try:
        from_date, to_date = get_from_date_to_date(request)
    except BadRequest, e:
        return bad_request(e)

    supports = Transaction.get_transactions_by_dates(user['id'], whose, 'support', from_date, to_date)

    return ok_raw(supports)


@api_view(['GET'])
@authorization_needed
def transactions(request, whose, user):
    logger.info('METHOD: transactions')

    try:
        limit, offset = get_limit_and_offset(request)
    except BadRequest, e:
        return bad_request(e)

    transactions = Transaction.get_transactions_by_offset(user['id'], whose, limit, offset)

    return ok_raw(transactions)

# supports
@api_view(['POST'])
@authorization_needed
def post_support(request, user):
    logger.info('METHOD: post_support')

    try:
        uuid = request.data['uuid']
        amount = float(request.data['amount'])
        currency = request.data['currency']
        is_anonymous = get_boolean(request.data['is_anonymous'])
    except Exception, e:
        return bad_request(BadRequest(e))

    supported_user = User.find_by_user_uuid(uuid, scope='all')

    if not supported_user:
        return not_found(UserIsNotFound())

    try:
        transaction_id = Transaction.add_support(user['id'], supported_user['id'], amount, currency, is_anonymous)
    except NotEnoughMoneyException, e:
        return not_acceptable(e)

    return created(transaction_id=transaction_id)

# receives
@api_view(['GET'])
@authorization_needed
def receives(request, whose, user):
    logger.info('METHOD: receives')

    try:
        from_date, to_date = get_from_date_to_date(request)
    except BadRequest, e:
        return bad_request(e)

    # getting data
    receives = Transaction.get_transactions_by_dates(user['id'], whose, 'receive', from_date, to_date)

    return ok_raw(receives)

# statistics
@api_view(['GET'])
@authorization_needed
def statistics_overall(request, user_uuid, user):
    logger.info('METHOD: statistics_overall')

    if user_uuid == 'my':
        user_uuid = user['uuid']
        statistics_user = user
    else:
        statistics_user = User.find_by_user_uuid(user_uuid, scope='all')

    if not statistics_user:
        return not_found(UserIsNotFound())

    # getting data
    statistics = Statistics.get_statistics_overall(statistics_user['id'])

    return ok_raw(statistics)

# statistics
@api_view(['GET'])
@authorization_needed
def statistics_counter_users(request, transaction_direction, user_uuid, user):
    logger.info('METHOD: statistics_counter_users')

    #
    if transaction_direction == 'supports':
        transaction_direction = 'support'
    else:
        transaction_direction = 'receive'

    #
    try:
        limit, offset = get_limit_and_offset(request)
    except Exception, e:
        return bad_request(BadRequest(e))

    #
    if user_uuid == 'my':
        user_uuid = user['uuid']
        statistics_user = user
    else:
        statistics_user = User.find_by_user_uuid(user_uuid, scope='all')

    # 404?
    if not statistics_user:
        return not_found(UserIsNotFound())

    # getting data
    statistics = Statistics.get_statistics_counter_users(statistics_user['id'], transaction_direction, limit, offset)

    return ok_raw(statistics)

# list of notifications or delete them all
@api_view(['GET', 'DELETE'])
@authorization_needed
def notifications(request, user):
    logger.info('METHOD: notifications')

    if request.method == 'GET':
        #input
        try:
            limit, offset = get_limit_and_offset(request)
        except Exception, e:
            return bad_request(BadRequest(e))

        notifications = Notification.get_notifications_by_user_id(user['id'], limit, offset)

        return ok_raw(notifications)

    elif request.method == 'DELETE':
        Notification.delete_all_notifications_by_user_id(user['id'])

        return no_content()

# delete notification
@api_view(['DELETE'])
@authorization_needed
def notification(request, notification_id, user):
    logger.info('METHOD: notification')

    try:
        Notification.delete_notification(user['id'], notification_id)
    except ResourceIsNotFound, e:
        return not_found(e)

    return no_content()

# graph
@api_view(['GET'])
@authorization_needed
def graph(request, user):
    logger.info('METHOD: graph')

    me_id = user['id']
    me = User.get_by_id(me_id, scope='graph')
    me['follows'] = Graph.get_follows(me_id)
    me['followed_by'] = Graph.get_followed_by(me_id)

    return ok_raw({
        'users_counts': Graph.get_users_counts(),
        'zero_generation': Graph.get_zero_generation(),
        'me': me,
    })

def render_graph_user(user_id):
    user = User.get_by_id(user_id, scope='graph')
    user['follows'] = Graph.get_follows(user_id)
    user['followed_by'] = Graph.get_followed_by(user_id)
    return ok_raw(user)

# graph user by uuid
@api_view(['GET'])
@authorization_needed
def graph_user_by_uuid(request, user_uuid, user):
    logger.info('METHOD: graph_user')

    if user_uuid != 'me':
        graph_user = User.find_by_user_uuid(user_uuid, scope='all')
        if not graph_user:
            return not_found(UserIsNotFound())
    else:
        graph_user = user

    return render_graph_user(graph_user['id'])

# graph user by num_in_generation
@api_view(['GET'])
@authorization_needed
def graph_user(request, user):
    logger.info('METHOD: graph_user_by_num_in_generation')

    generation = request.GET.get('generation')
    num_in_generation = request.GET.get('num_in_generation')

    user_id = User.get_user_id_by_num_in_generation(generation, num_in_generation)

    if not user_id:
        return not_found(UserIsNotFound())

    return render_graph_user(user_id)

# deposits
@api_view(['POST'])
@authorization_needed
def post_deposit(request, user):
    logger.info('METHOD: post_deposit')

    try:
        provider = request.data['provider']
        provider_transaction_id = request.data['provider_transaction_id']
        amount = float(request.data['amount'])
        currency = request.data['currency']
    except:
        return bad_request(BadRequest(None))

    try:
        transaction_id = Transaction.add_deposit(user['id'], provider, provider_transaction_id, amount, currency)
        return created(transaction_id=transaction_id)
    except ConflictException, e:
        return conflict()
    except ResourceIsNotFound, e:
        return not_acceptable(e)
    except NotAcceptableException, e:
        return not_acceptable(e)

# withdrawals
@api_view(['GET', 'POST'])
@authorization_needed
def withdrawal_requests(request, user):
    logger.info('METHOD: withdrawal_requests')

    if request.method == 'POST':
        try:
            provider = request.data['provider']
            amount = float(request.data['amount'])
            currency = request.data['currency']
            email = None
            if provider == 'paypal':
                email = request.data['email']
        except:
            return bad_request(BadRequest(None))

        try:
            request_id = WithdrawalRequest.add_withdrawal_request(
                user['id'],
                amount, currency,
                provider, {'email': email}
            )
            return created(request_id=request_id)
        except NotEnoughMoneyException, e:
            return not_acceptable(e)
        except InvalidEmail, e:
            return bad_request(e)

    elif request.method == 'GET':
        try:
            limit, offset = get_limit_and_offset(request)
        except BadRequest, e:
            return bad_request(e)

        requests = WithdrawalRequest.get_withdrawal_requests_by_user_id(user['id'], limit, offset)

        return ok_raw(requests)

