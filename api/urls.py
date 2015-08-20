from django.conf.urls import url
from api import views

urlpatterns = [
    url(r'v1/session', views.session),
    url(r'v1/user/(?P<user_uuid>[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})', views.user),
    url(r'v1/profile', views.profile),
]
