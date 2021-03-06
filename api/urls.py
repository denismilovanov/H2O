from django.conf.urls import url
from api import views

urlpatterns = [
    # error
    url(r'v1/error/(?P<http_code>\d+)', views.error),
    # params
    url(r'v1/params', views.params),

    # sessions and users
    url(r'v1/session', views.session),
    url(r'v1/users/(?P<user_uuid>([0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})|me)', views.user),
    url(r'v1/profile', views.profile),

    # invites
    url(r'v1/invite_codes/(?P<invite_code>[0-9a-zA-Z_]+)', views.invite_code),
    url(r'v1/invite_codes', views.invite_codes),

    # add follow (post)
    # get smbd's follow (get)
    url(r'v1/follows/(?P<user_uuid>[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})', views.follow),
    # get my follows
    url(r'v1/follows/(?P<user_uuid>my)', views.follows),

    # supports
    url(r'v1/supports', views.post_support),
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
    url(r'v1/graph/users/(?P<user_uuid>(me|[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}))', views.graph_user_by_uuid),
    url(r'v1/graph/users', views.graph_user),
    url(r'v1/graph', views.graph),

    # deposits
    url(r'v1/deposits', views.post_deposit),

    # withdrawals
    url(r'v1/withdrawal_requests', views.withdrawal_requests),

    # counts
    url(r'v1/counts/(?P<type>[a-z]+)', views.counts),

]
