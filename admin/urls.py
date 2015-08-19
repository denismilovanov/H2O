from django.conf.urls import url
from admin import views

urlpatterns = [
    url(r'admin/users', views.users),
    url(r'admin', views.index),
]
