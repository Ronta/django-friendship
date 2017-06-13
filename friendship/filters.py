try:
    from django.contrib.auth import get_user_model

    user_model = get_user_model()
except ImportError:
    from django.contrib.auth.models import User

    user_model = User

import django_filters

from rest_framework import filters
from friendship.models import Friend, FriendshipRequest


class FriendFilter(filters.FilterSet):
    to_user = django_filters.CharFilter(name="to_user__username", lookup_expr='icontains')
    from_user = django_filters.CharFilter(name="from_user__username", lookup_expr='icontains')

    class Meta:
        model = Friend
        fields = ['to_user', 'from_user']


class FriendshipFilter(filters.FilterSet):
    to_user = django_filters.CharFilter(name="to_user__username", lookup_expr='icontains')
    from_user = django_filters.CharFilter(name="from_user__username", lookup_expr='icontains')

    class Meta:
        model = FriendshipRequest
        fields = ['to_user', 'from_user']
