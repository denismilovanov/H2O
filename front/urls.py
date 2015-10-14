from django.conf.urls import url
from front import views

urlpatterns = [
    # iOS build requests
    url(r'request/ios', views.request_ios_build),
]

