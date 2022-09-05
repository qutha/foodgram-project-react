from django.contrib.auth import get_user_model

from djoser.views import UserViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from users.models import Follow
from users.serializers import (
    AllFieldsRequiredUserSerializer, SubscribeSerializer
)

User = get_user_model()


class AllFieldsRequiredUserViewSet(UserViewSet):
    """Представление для создания и получения пользователей,
    а также их подписок."""
    queryset = User.objects.all()
    pagination_class = PageNumberPagination

    def get_permissions(self):
        if self.action in ('list', 'create'):
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        if self.action in ('subscribe', 'subscriptions'):
            return SubscribeSerializer
        return AllFieldsRequiredUserSerializer

    @action(
        detail=True,
        methods=['POST', 'DELETE'],
        permission_classes=[IsAuthenticated],
    )
    def subscribe(self, request, id):
        follower = request.user
        following = get_object_or_404(User, id=id)

        if request.method == 'POST':
            if follower.id == following.id:
                return Response(
                    {'detail': 'Нельзя подписаться на самого себя.'},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            _, created = Follow.objects.get_or_create(
                user=follower, author=following,
            )

            if not created:
                return Response(
                    {'detail': 'Вы уже подписаны на этого пользователя.'},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            serializer = self.get_serializer(
                following, context=self.get_serializer_context(),
            )
            return Response(data=serializer.data, status=status.HTTP_200_OK)

        elif request.method == 'DELETE':
            is_follow_exists = Follow.objects.filter(
                user=follower, author=following,
            ).exists()
            if not is_follow_exists:
                return Response(
                    {'detail': 'Вы не подписаны на этого пользователя.'},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            Follow.objects.filter(
                user=follower, author=following,
            ).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=False,
        methods=['GET'],
        permission_classes=[IsAuthenticated],
    )
    def subscriptions(self, request):
        user = request.user
        following_users = User.objects.filter(following__user=user)

        page = self.paginate_queryset(following_users)
        if page is not None:
            serializer = self.get_serializer(
                page, context=self.get_serializer_context(), many=True,
            )
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(
            following_users, context=self.get_serializer_context(), many=True,
        )
        return Response(data=serializer.data, status=status.HTTP_200_OK)
