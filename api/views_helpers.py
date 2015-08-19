from django.http import HttpResponse
from rest_framework.renderers import JSONRenderer
from rest_framework import status

import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class JSONResponse(HttpResponse):
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)

def bad_request(e):
    v = {
        'error': e,
    }
    return HttpResponse(v, status=status.HTTP_400_BAD_REQUEST)

def internal_server_error(e):
    v = {
        'error': e,
    }
    return JSONResponse(v, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

def created(**v):
    return JSONResponse(v, status=status.HTTP_201_CREATED)

def unauthorized(e):
    v = {
        'error': str(e)
    }
    return JSONResponse(v, status=status.HTTP_401_UNAUTHORIZED)

def forbidden(e):
    v = {
        'error': str(e)
    }
    return JSONResponse(v, status=status.HTTP_403_FORBIDDEN)

def not_found(e):
    v = {
        'error': str(e)
    }
    return HttpResponse(v, status=status.HTTP_404_NOT_FOUND)

def unavailable(e):
    v = {
        'error': str(e)
    }
    return HttpResponse(v, status=status.HTTP_503_SERVICE_UNAVAILABLE)

def not_acceptable(e):
    v = {
        'error': str(e)
    }
    return JSONResponse(v, status=status.HTTP_406_NOT_ACCEPTABLE)

def no_content():
    return HttpResponse(status=status.HTTP_204_NO_CONTENT)

def ok(**v):
    return JSONResponse(v)
