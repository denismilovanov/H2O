from rest_framework.decorators import api_view
from views_helpers import created, bad_request, unavailable, forbidden, unauthorized, ok, ok_raw, internal_server_error, not_found, not_acceptable, no_content
from models import *
from models.exceptions import *

import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# decorator for all methods
def authorization_needed(func):
    def inner(*k, **v):
        logger.debug('METHOD: authorization_needed')

        request = k[0]

        # get token
        try:
            access_token = request.META.get('HTTP_ACCESS_TOKEN')
            if not access_token:
                access_token = request.META['headers']['Access-Token']

            logger.debug('access token ' + str(access_token))
        except Exception, e:
            return unauthorized(e)

        # get user
        try:
            user = User.find_by_access_token(access_token)
            if not user:
                return unauthorized(access_token)
        except Exception, e:
            return internal_server_error(e)

        # pass user
        v['user'] = user

        # call decorated function
        try:
            return func(*k, **v)
        except Exception, e:
            return internal_server_error(e)

    return inner

# session
@api_view(['POST', 'PATCH'])
def session(request):
    logger.debug('METHOD: session')
    logger.debug(request.data)

    # new session
    if request.method == 'POST':
        #input
        try:
            network_id = request.data.get('network_id')
            access_token = request.data.get('access_token')
            invite_code = request.data.get('invite_code')

            logger.debug(request.data)
        except Exception, e:
            return bad_request(e)

        # connecting to facebook
        try:
            user_data = User.get_user_via_network(network_id, access_token)
        except FacebookException, e:
            return unavailable(e)
        except Exception, e:
            return forbidden(e)

        # creating or getting user
        try:
            user = User.upsert(user_data, network_id, access_token, invite_code)
        except (InviteCodeAlreadyTakenException, InviteCodeDoesNotExistException), e:
            return forbidden(e)
        except Exception, e:
            return internal_server_error(e)

        # creating session
        try:
            session = User.get_session(user['user_uuid'])
        except Exception, e:
            return internal_server_error(e)

        # result
        return created(user=user, session=session)

    # refresh session
    elif request.method == 'PATCH':
        try:
            refresh_token = request.data['refresh_token']
        except Exception, e:
            return bad_request(e)

        access_token = User.refresh_access_token(refresh_token)

        if not access_token:
            return unauthorized('Refresh token is old')

        from H2O.settings import ACCESS_TOKEN_EXPIRES_IN
        return ok(access_token=access_token, access_token_expires_in=ACCESS_TOKEN_EXPIRES_IN)

# profile
@api_view(['GET'])
@authorization_needed
def user(request, user_uuid, user):
    logger.debug('METHOD: user')

    user = User.find_by_user_uuid(user_uuid, scope='public_profile')

    if not user: # or user['is_deleted']:
        return not_found(user_uuid)

    return ok(user=user)

# list of user
@api_view(['GET'])
@authorization_needed
def users(request, user):
    logger.debug('METHOD: users')

    users = User.get_all(1000, 0, scope='public_all')

    return ok_raw(users)

# profile
@api_view(['PATCH'])
@authorization_needed
def profile(request, user):
    logger.debug('METHOD: profile')

    #input
    try:
        visibility = request.data.get('visibility')
        status = request.data.get('status')

        logger.debug(request.data)
    except Exception, e:
        return bad_request(e)

    User.update_profile(user['id'], visibility, status)

    return no_content()

# invite codes list
@api_view(['GET'])
@authorization_needed
def invite_codes(request, user):
    logger.debug('METHOD: invite_codes')

    return ok_raw(Invite.get_invite_codes_by_user_id(user['id'], scope='public_invite_codes'))


# update invite code
@api_view(['PATCH'])
@authorization_needed
def invite_code(request, invite_code, user):
    logger.debug('METHOD: invite_code')

    #input
    try:
        email = request.data['email']
    except Exception, e:
        return bad_request(e)

    # get code
    code = Invite.get_invite_code(invite_code)
    logger.debug(code)

    if not code or code['status'] != 'free':
        # there is no code available
        return not_found(invite_code)

    if code['owner_id'] != user['id']:
        # code is not mine
        return forbidden(invite_code)

    # making invite
    try:
        Invite.invite_user_via_invite_code_and_email(invite_code, email)
    except InvalidEmail, e:
        return bad_request(e)
    except EmailIsAlreadyUsed, e:
        return not_acceptable(e)

    return no_content()
