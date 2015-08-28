from rest_framework.decorators import api_view
from views_helpers import created, bad_request, unavailable, forbidden, unauthorized, ok, ok_raw, internal_server_error, not_found, not_acceptable, no_content
from models import *
from models.exceptions import *
import datetime

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# decorator for all methods
def authorization_needed(func):
    def inner(*k, **v):
        request = k[0]
        refresh_token = request.data.get('refresh_token')
        access_token = None
        user = {}

        if  not refresh_token and \
            not (request.path == '/v1/session' and request.method == 'POST'):

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

# session
@api_view(['POST', 'PATCH'])
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
            access_token = UserSession.refresh_access_token(refresh_token)

            if not access_token:
                return unauthorized(ResfreshTokenDoesNotExist())

            from H2O.settings import ACCESS_TOKEN_EXPIRES_IN
            return ok(access_token=access_token, access_token_expires_in=ACCESS_TOKEN_EXPIRES_IN)

        if push_token:
            UserSession.update_push_token(user['id'], user['access_token'], push_token)

            return no_content()

# profile
@api_view(['GET'])
@authorization_needed
def user(request, user_uuid, user):
    logger.info('METHOD: user')

    user = User.find_by_user_uuid(user_uuid, scope='public_profile')

    if not user: # or user['is_deleted']:
        return not_found(user_uuid)

    return ok_raw(user)

# list of user
@api_view(['GET'])
@authorization_needed
def users(request, user):
    logger.info('METHOD: users')

    users = User.get_all(1000, 0, scope='public_profile')

    return ok_raw(users)

# profile
@api_view(['PATCH'])
@authorization_needed
def profile(request, user):
    logger.info('METHOD: profile')

    #input
    try:
        visibility = request.data.get('visibility')
        status = request.data.get('status')
        logger.info(request.data)

    except Exception, e:
        return bad_request(BadRequest(e))

    User.update_profile(user['id'], visibility, status)

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
    except Exception, e:
        return bad_request(BadRequest(e))

    # get code
    code = Invite.get_invite_code(invite_code)
    logger.info(code)

    if not code or code['status'] != 'free':
        # there is no code available
        return not_found(InviteCodeDoesNotExistException())

    if code['owner_id'] != user['id']:
        # code is not mine
        return forbidden(InviteCodeDoesNotExistException())

    # making invite
    try:
        Invite.invite_user_via_invite_code_and_email(invite_code, email)
    except InvalidEmail, e:
        return bad_request(e)
    except EmailIsAlreadyUsed, e:
        return not_acceptable(e)

    return no_content()

# add follow
@api_view(['GET', 'POST'])
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
        limit = request.data.get('limit', 20)
        offset = request.data.get('offset', 0)

        if limit < 0:
            limit = 20

        if offset < 0:
            offset = 0

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
    follows = UserFollow.get_user_follows(user_id, limit, offset)

    # if we need to get list of other user's follows
    # then we shall calculate i_follow
    if user['id'] != user_id:
        my_follows = UserFollow.get_user_follows(user['id'], int(1e6), 0)

        my_follows_uuids = [my_follow['uuid'] for my_follow in my_follows]

        for follow in follows:
            follow['i_follow'] = follow['uuid'] in my_follows_uuids
    else:
        for follow in follows:
            follow['i_follow'] = False

    # that's all
    return ok_raw(follows)

# supports
@api_view(['GET'])
@authorization_needed
def supports(request, whose, user):
    logger.info('METHOD: supports')

    try:
        from_date = request.GET['from_date']
        to_date = request.GET['to_date']
    except Exception, e:
        return bad_request(BadRequest(e))

    # special dates
    if from_date == 'now':
        from_date = str(datetime.datetime.now().date())
    if to_date == 'now':
        to_date = str(datetime.datetime.now().date())

    logger.info(from_date)
    logger.info(to_date)

    # parse string repr
    try:
        from dateutil.parser import parse
        from_date = parse(from_date)
        to_date = parse(to_date)
    except Exception, e:
        return bad_request(BadRequest(e))

    # getting data
    supports = []

    if whose == 'my':
        supports = Transaction.get_my_supports(user['id'], from_date, to_date)
    elif whose == 'follows':
        supports = Transaction.get_follows_supports(user['id'], from_date, to_date)

    return ok_raw(supports)
