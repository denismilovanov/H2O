from django.conf.urls import url
from api import views

urlpatterns = [
    # error
    url(r'v1/error/(?P<http_code>\d+)', views.error),

    # sessions and users
    url(r'v1/session', views.session),
    url(r'v1/users/(?P<user_uuid>([0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})|me)', views.user),
    url(r'v1/users', views.users),
    url(r'v1/profile', views.profile),

    # invites
    url(r'v1/invite_codes/(?P<invite_code>[0-9a-zA-Z]+)', views.invite_code),
    url(r'v1/invite_codes', views.invite_codes),

    # add follow (post)
    # get smbd's follow (get)
    url(r'v1/follows/(?P<user_uuid>[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})', views.follow),
    # get my follows
    url(r'v1/follows/(?P<user_uuid>my)', views.follows),

    # supports
    url(r'v1/supports/(?P<whose>(my|follows))', views.supports),
    url(r'v1/supports', views.post_support),
    # receives
    url(r'v1/receive(d|s)/(?P<whose>(my|follows))', views.receives),
    # transactions
    url(r'v1/transactions/(?P<whose>(my|follows))', views.transactions),

    # statistics
    url(r'v1/statistics/(?P<user_uuid>(my|[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}))/overall', views.statistics_overall),

    # statistics: counter users
    url(r'v1/statistics/(?P<user_uuid>(my|[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}))/counter_users/(?P<transaction_direction>supports|receives)', views.statistics_counter_users),

    # notifications
    url(r'v1/notifications/(?P<notification_id>\d+)', views.notification),
    url(r'v1/notifications', views.notifications),

    # graph
    url(r'v1/graph/(?P<user_uuid>(me|[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}))', views.graph_user),
    url(r'v1/graph', views.graph),

    # deposits
    url(r'v1/deposits', views.post_deposit),

]
