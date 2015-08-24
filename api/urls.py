from django.conf.urls import url
from api import views

urlpatterns = [
    url(r'v1/session', views.session),
    url(r'v1/users/(?P<user_uuid>[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})', views.user),
    url(r'v1/users', views.users),
    url(r'v1/profile', views.profile),
    url(r'v1/invite_codes/(?P<invite_code>[0-9a-zA-Z]+)', views.invite_code),
    url(r'v1/invite_codes', views.invite_codes),
    url(r'v1/follows/(?P<user_uuid>[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})', views.follow),
    url(r'v1/follows', views.follows),
]