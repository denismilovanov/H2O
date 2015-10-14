from django.conf.urls import include, url

urlpatterns = [
    url(r'', include('api.urls')),
    url(r'', include('admin.urls')),
    url(r'', include('front.urls')),
]

