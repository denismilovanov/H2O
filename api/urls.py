from django.conf.urls import url
from api import views

urlpatterns = [
    url(r'v1/session', views.session),
    url(r'v1/users/(?P<user_uuid>[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})', views.user),
    url(r'v1/users', views.users),
    url(r'v1/profile', views.profile),
    url(r'v1/invite_codes/(?P<invite_code>[0-9a-zA-Z]+)', views.invite_code),
    url(r'v1/invite_codes', views.invite_codes),
    # add follow (post)
    # get smbd's follow (get)
    url(r'v1/follows/(?P<user_uuid>[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})', views.follow),
    # get my follows
    url(r'v1/follows/(?P<user_uuid>my)', views.follows),

    # supports
    url(r'v1/supports/(?P<whose>(my|follows))', views.supports),
    # receives
    url(r'v1/receives/(?P<whose>(my|follows))', views.receives),
]
