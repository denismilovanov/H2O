from django.conf.urls import url
from admin import views

urlpatterns = [
    url(r'admin', views.index),
]
