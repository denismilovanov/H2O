from django.conf.urls import include, url
from api import views

urlpatterns = [
    url(r'', include('api.urls')),
    url(r'', include('admin.urls')),
]

