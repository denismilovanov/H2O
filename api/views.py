from rest_framework.decorators import api_view
from views_helpers import created, bad_request, unavailable, forbidden, unauthorized, ok, internal_server_error, not_found, not_acceptable, no_content
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
            credentials = request.data['credentials']
            network_id = credentials['network_id']
            user_id = credentials['user_id']
            access_token = credentials['access_token']
            logger.debug(credentials)

            invite_code = request.data.get('invite_code')
            logger.debug(invite_code)
        except Exception, e:
            return internal_server_error(e)

        # connecting to facebook
        try:
            user_data = User.get_user_via_network(network_id, user_id, access_token)
        except FacebookException, e:
            return unavailable(e)
        except Exception, e:
            return forbidden(e)

        # creating or getting user
        try:
            user = User.upsert(user_data, network_id, user_id, access_token, invite_code)
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

        return ok(access_token=access_token)

# profile
@api_view(['GET'])
@authorization_needed
def user(request, user_uuid, user):
    logger.debug('METHOD: user')

    user = User.find_by_user_uuid(user_uuid, scope='public_profile')

    if not user: # or user['is_deleted']:
        return not_found(user_uuid)

    return ok(user=user)

