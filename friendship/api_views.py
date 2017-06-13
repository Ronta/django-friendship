from django.core.exceptions import ObjectDoesNotExist

from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


from .serializers import FriendshipRequestSerializers, FriendSerializers

from friendship.models import FriendshipRequest, Friend
from friendship.exceptions import AlreadyExistsError, AlreadyFriendsError
from friendship.filters import FriendFilter, FriendshipFilter

try:
    from django.contrib.auth import get_user_model

    user_model = get_user_model()
except ImportError:
    from django.contrib.auth.models import User

    user_model = User


class FriendshipRequestViewSet(generics.ListAPIView):
    queryset = FriendshipRequest.objects.all()
    serializer_class = FriendshipRequestSerializers
    permission_classes = IsAuthenticated
    filter_class = FriendshipFilter

    def get_queryset(self):
        qs = super().get_queryset().filter(to_user=self.request.user)
        for friendship in qs:
            friendship.mark_viewed()
        return qs


class FriendsApiViewset(generics.ListAPIView):
    queryset = Friend.objects.all()
    serializer_class = FriendSerializers
    permission_classes = IsAuthenticated
    filter_class = FriendFilter

    def get_queryset(self):
        # TODO Is horrible, but with this solution i use the base manager.
        friends_list = Friend.objects.friends(user=self.request.user)
        return Friend.objects.filter(from_user__id__in=[u.id for u in friends_list])


class FriendshipAddFriendViewset(generics.CreateAPIView):
    queryset = Friend.objects.all()
    permission_classes = IsAuthenticated
    serializer_class = FriendshipRequestSerializers

    def create(self, request, *args, **kwargs):
        try:
            to_user = user_model.objects.get(id=kwargs['to_username'])
        except ObjectDoesNotExist:
            response_data = {"detail": "User not exist"}
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

        from_user = self.request.user

        try:
            data = {
                'to_user': to_user.pk,
                'from_user': from_user.pk,
            }
            serializer = self.get_serializer(data=data)
            serializer.is_valid(raise_exception=True)

            f_request_status = self._add_friends_request(from_user=from_user, to_user=to_user)
            if f_request_status['error']:
                response_data = {"detail": f_request_status['detail']}
                return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        except AlreadyExistsError as e:
            errors = ["%s" % e]
            response_data = {"detail": errors}
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

    def _add_friends_request(self, from_user, to_user):
        try:
            Friend.objects.add_friend(from_user, to_user)
            status = {
                'error': False
            }
            return status
        except AlreadyFriendsError:
            status = {'detail' : "Users are already friends",
                      'error': True
            }
            return status


class FriendshipAcceptFriendViewset(generics.CreateAPIView):
    queryset = FriendshipRequest.objects.all()
    permission_classes = IsAuthenticated
    serializer_class = FriendshipRequestSerializers

    def create(self, request, *args, **kwargs):
        try:
            f_request = self.queryset.get(id=kwargs['friendship_request_id'],
                                          to_user=self.request.user)
        except ObjectDoesNotExist:
            response_data = {"detail": "Friendship request not exist"}
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

        if f_request.accept():
            return Response({}, status=status.HTTP_204_NO_CONTENT)
        else:
            response_data = {"detail": "Ho perso una nutria tra i server"}
            return Response(response_data, status=status.HTTP_201_CREATED)


class FriendshipRejectFriendViewset(generics.CreateAPIView):
    queryset = FriendshipRequest.objects.all()
    permission_classes = IsAuthenticated
    serializer_class = FriendshipRequestSerializers

    def create(self, request, *args, **kwargs):
        try:
            f_request = self.queryset.get(id=kwargs['friendship_request_id'],
                                          to_user=self.request.user)
        except ObjectDoesNotExist:
            response_data = {"detail": "Friendship request not exist"}
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

        if f_request.reject():
            return Response({}, status=status.HTTP_204_NO_CONTENT)
        else:
            response_data = {"detail": "Ho perso una nutria tra i server"}
            return Response(response_data, status=status.HTTP_201_CREATED)


class FriendshipCancelFriendViewset(generics.CreateAPIView):
    queryset = FriendshipRequest.objects.all()
    permission_classes = IsAuthenticated
    serializer_class = FriendshipRequestSerializers

    def create(self, request, *args, **kwargs):
        try:
            f_request = self.queryset.get(id=kwargs['friendship_request_id'],
                                          to_user=self.request.user)
        except ObjectDoesNotExist:
            response_data = {"detail": "Friendship request not exist"}
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

        if f_request.cancel():
            return Response({}, status=status.HTTP_204_NO_CONTENT)
        else:
            response_data = {"detail": "Ho perso una nutria tra i server"}
            return Response(response_data, status=status.HTTP_201_CREATED)


class FriendsRemoveViewset(generics.DestroyAPIView):
    queryset = Friend.objects.all()
    permission_classes = IsAuthenticated
    serializer_class = FriendSerializers

    def delete(self, request, *args, **kwargs):
        try:
            to_user = user_model.objects.get(pk=kwargs['to_user'])
        except ObjectDoesNotExist:
            response_data = {"detail": "User not exist"}
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

        if Friend.objects.remove_friend(from_user=self.request.user, to_user=to_user):
            return Response({}, status=status.HTTP_204_NO_CONTENT)
        else:
            response_data = {"detail": "User are not Friends"}
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)


class AreFriendsVieset(generics.GenericAPIView):
    queryset = Friend.objects.all()
    permission_classes = IsAuthenticated
    serializer_class = FriendSerializers
    http_method_names = ['get']

    def get(self, request, *args, **kwargs):
        try:
            user2 = user_model.objects.get(pk=kwargs['to_user'])
        except ObjectDoesNotExist:
            response_data = {"detail": "User not exist"}
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

        if Friend.objects.are_friends(user1=self.request.user, user2=user2):
            response_data = {"detail": "User are friends"}
            return Response(response_data, status=status.HTTP_200_OK)
        else:
            response_data = {"detail": "User are not friends"}
            return Response(response_data, status=status.HTTP_200_OK)
