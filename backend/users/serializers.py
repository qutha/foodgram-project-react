from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers

from recipes.serializers import RecipeMinimizedSerializer

User = get_user_model()


class AllFieldsRequiredUserCreateSerializer(UserCreateSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'username',
            'first_name',
            'last_name',
            'password',
        )


class AllFieldsRequiredUserSerializer(UserSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
        )

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        user = request.user
        if user.is_authenticated:
            return user.follower.filter(author=obj).exists()
        return False


class SubscribeSerializer(AllFieldsRequiredUserSerializer):
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
            'recipes_count',
        )

    def get_recipes(self, data):
        request = self.context.get('request')
        recipes_limit = request.GET.get('recipes_limit')
        if recipes_limit:
            try:
                recipes = data.recipes.all()[:int(recipes_limit)]
            except ValueError:
                recipes = data.recipes.all()
        else:
            recipes = data.recipes.all()
        serializer = RecipeMinimizedSerializer(recipes, many=True)
        return serializer.data

    def get_recipes_count(self, data):
        return data.recipes.count()
