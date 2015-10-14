from models import *
from models.exceptions import *
from django.shortcuts import render_to_response
from django.template import RequestContext


import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def request_ios_build(request):
    status = False
    if request.method == 'GET':
        # get email and code
        email = request.GET.get('email')
        invite_code = request.GET.get('invite_code')

        # get invite from db
        invite = Invite.get_invite_code_by_email(email)

        # check
        if invite and invite['invite_code'] == invite_code:
            # all correct
            status = Invite.request_ios_build(invite['owner_id'], invite_code)
        else:
            pass


    return render_to_response('index.html', {
        'email': email,
        'invite_code': invite_code,
        'status': status,
    }, RequestContext(request))

