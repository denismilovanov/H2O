# django stuff
from django.shortcuts import redirect
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError

from django.http import HttpResponse, Http404
from django.shortcuts import render_to_response
from django.template import RequestContext

# models
from models import *

# decorators
from decorators import *


def index(request):
    # action = request.GET.get('action', '')
    # return HttpResponse('{"result":' + str(result) + '}', content_type='application/json')

    return render_to_response('index.html', {
        # nothing
    }, RequestContext(request))


def users(request):
    limit = request.GET.get('limit', 20)
    offset = request.GET.get('offset', 0)

    return render_to_response('users/users.html', {
        'users': User.get_all(limit=limit, offset=offset, scope='admin')
    }, RequestContext(request))


