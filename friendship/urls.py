try:
    from django.conf.urls import url, include
except ImportError:
    from django.conf.urls.defaults import url, include

from friendship.views import view_friends, friendship_add_friend, friendship_accept, \
    friendship_reject, friendship_cancel, friendship_request_list, \
    friendship_request_list_rejected, friendship_requests_detail, followers,\
    following, follower_add, follower_remove, all_users

from friendship.api_views import FriendshipRequestViewSet, FriendsApiViewset, \
    FriendshipAddFriendViewset, FriendshipAcceptFriendViewset, FriendshipRejectFriendViewset, \
    FriendshipCancelFriendViewset, FriendsRemoveViewset, AreFriendsVieset

# router = routers.DefaultRouter()
# router.register(r'api/friend/requests', FriendshipRequestViewSet.as_view())

urlpatterns = [
    url(
        regex=r'^users/$',
        view=all_users,
        name='friendship_view_users',
    ),
    url(
        regex=r'^friends/(?P<username>[\w-]+)/$',
        view=view_friends,
        name='friendship_view_friends',
    ),
    url(
        regex=r'^friend/add/(?P<to_username>[\w-]+)/$',
        view=friendship_add_friend,
        name='friendship_add_friend',
    ),
    url(
        regex=r'^friend/accept/(?P<friendship_request_id>\d+)/$',
        view=friendship_accept,
        name='friendship_accept',
    ),
    url(
        regex=r'^friend/reject/(?P<friendship_request_id>\d+)/$',
        view=friendship_reject,
        name='friendship_reject',
    ),
    url(
        regex=r'^friend/cancel/(?P<friendship_request_id>\d+)/$',
        view=friendship_cancel,
        name='friendship_cancel',
    ),
    url(
        regex=r'^friend/requests/$',
        view=friendship_request_list,
        name='friendship_request_list',
    ),
    url(
        regex=r'^friend/requests/rejected/$',
        view=friendship_request_list_rejected,
        name='friendship_requests_rejected',
    ),
    url(
        regex=r'^friend/request/(?P<friendship_request_id>\d+)/$',
        view=friendship_requests_detail,
        name='friendship_requests_detail',
    ),
    url(
        regex=r'^followers/(?P<username>[\w-]+)/$',
        view=followers,
        name='friendship_followers',
    ),
    url(
        regex=r'^following/(?P<username>[\w-]+)/$',
        view=following,
        name='friendship_following',
    ),
    url(
        regex=r'^follower/add/(?P<followee_username>[\w-]+)/$',
        view=follower_add,
        name='follower_add',
    ),
    url(
        regex=r'^follower/remove/(?P<followee_username>[\w-]+)/$',
        view=follower_remove,
        name='follower_remove',
    ),
    # ReST Framwork
    url(r'^api-auth/',
        include('rest_framework.urls',
                namespace='rest_framework')),

    url(regex=r'api/friend/requests/$',
        view=FriendshipRequestViewSet.as_view(),
        name='api_friendship_request_list'
        ),
    url(regex=r'^api/friends/$',
        view=FriendsApiViewset.as_view(),
        name='api_friendship_view_friends'
        ),
    url(regex=r'^api/friends/add/(?P<to_username>[\w-]+)/$',
        view=FriendshipAddFriendViewset.as_view(),
        name='api_friendship_add_friend'
        ),
    url(regex=r'^api/friends/accept/(?P<friendship_request_id>\d+)/$',
        view=FriendshipAcceptFriendViewset.as_view(),
        name='api_friendship_accept'
        ),
    url(
        regex=r'^api/friends/reject/(?P<friendship_request_id>\d+)/$',
        view=FriendshipRejectFriendViewset.as_view(),
        name='api_friendship_reject',
    ),
    url(
        regex=r'^api/friends/cancel/(?P<friendship_request_id>\d+)/$',
        view=FriendshipCancelFriendViewset.as_view(),
        name='api_friendship_cancel',
    ),
    url(
        regex=r'^api/friends/remove/(?P<to_user>\d+)/$',
        view=FriendsRemoveViewset.as_view(),
        name='api_friends_remove',
    ),
    url(
        regex=r'^api/friends/relationship/(?P<to_user>\d+)/$',
        view=AreFriendsVieset.as_view(),
        name='api_friends_detail',
    ),
]
