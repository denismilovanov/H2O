from django.http import HttpResponse
from rest_framework.renderers import JSONRenderer
from rest_framework import status

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class JSONResponse(HttpResponse):
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)

def bad_request(e, data=None):
    logger.info(e)
    from models.exceptions import BadRequestException
    v = {
        'error': str(e),
        'additional_data': str(e.e) if type(e) is BadRequestException else None,
    }
    if data:
        logger.info(data)
        v['data'] = data

    return JSONResponse(v, status=status.HTTP_400_BAD_REQUEST)

def internal_server_error(e):
    logger.info(e)
    v = {
        'error': 'INTERNAL_SERVER_ERROR',
    }

    # send exception to developers
    from tasks.send_exception_task import SendExceptionTask
    SendExceptionTask(e).enqueue()

    # output
    return JSONResponse(v, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

def created(**v):
    logger.info('CREATED')
    logger.info(v)
    return JSONResponse(v, status=status.HTTP_201_CREATED)

def unauthorized(e):
    logger.info(e)
    v = {
        'error': str(e)
    }
    return JSONResponse(v, status=status.HTTP_401_UNAUTHORIZED)

def forbidden(e, data=None):
    logger.info(e)
    v = {
        'error': str(e)
    }
    if data:
        logger.info(data)
        v['data'] = data

    return JSONResponse(v, status=status.HTTP_403_FORBIDDEN)

def not_found(e, data=None):
    logger.info(e)
    v = {
        'error': str(e)
    }
    if data:
        logger.info(data)
        v['data'] = data

    return JSONResponse(v, status=status.HTTP_404_NOT_FOUND)

def unavailable(e):
    logger.info(e)
    v = {
        'error': str(e)
    }
    return JSONResponse(v, status=status.HTTP_503_SERVICE_UNAVAILABLE)

def not_acceptable(e, data=None):
    logger.info(e)
    v = {
        'error': str(e)
    }
    if data:
        logger.info(data)
        v['data'] = data

    return JSONResponse(v, status=status.HTTP_406_NOT_ACCEPTABLE)

def no_content():
    logger.info('no content')
    return HttpResponse(status=status.HTTP_204_NO_CONTENT)

def conflict():
    logger.info('conflict')
    return HttpResponse(status=status.HTTP_409_CONFLICT)

def gone(e):
    logger.info('gone')
    return HttpResponse(status=status.HTTP_410_GONE)

def locked(e):
    logger.info('locked')
    return HttpResponse(status=status.HTTP_423_LOCKED)

def ok(**v):
    logger.info('OK')
    logger.info(v)
    return JSONResponse(v)

def ok_raw(v):
    logger.info('OK')
    logger.info(v)
    return JSONResponse(v)
