from rest_framework import serializers

from friendship.models import FriendshipRequest, Friend

try:
    from django.contrib.auth import get_user_model

    user_model = get_user_model()
except ImportError:
    from django.contrib.auth.models import User

    user_model = User


class DefaultUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = user_model
        fields = ('id', 'username')


class FriendshipRequestSerializers(serializers.ModelSerializer):

    to_user = DefaultUserSerializer()
    from_user = DefaultUserSerializer()

    class Meta:
        model = FriendshipRequest
        fields = ('from_user', 'to_user', 'message', 'created', 'rejected', 'viewed')


class FriendSerializers(serializers.ModelSerializer):
    to_user = DefaultUserSerializer()
    from_user = DefaultUserSerializer()

    class Meta:
        model = Friend
        fields = ('to_user', 'from_user')


