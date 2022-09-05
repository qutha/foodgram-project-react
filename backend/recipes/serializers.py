from django.contrib.auth import get_user_model
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers

from recipes.models import (
    Tag, Ingredient, Recipe, IngredientRecipe,
    TagRecipe, ShoppingCart, FavoriteRecipe,
)

User = get_user_model()


class AuthorSerializer(serializers.ModelSerializer):
    """Сериализатор для автора рецепта."""
    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'username',
            'first_name',
            'last_name',
        )


class TagSerializer(serializers.ModelSerializer):
    """Сериализатор для тегов рецепта."""
    class Meta:
        model = Tag
        fields = (
            'id',
            'name',
            'color',
            'slug',
        )


class IngredientSerializer(serializers.ModelSerializer):
    """Сериализатор для ингрединтов."""
    class Meta:
        model = Ingredient
        fields = (
            'id',
            'name',
            'measurement_unit',
        )


class IngredientRecipeSerializer(serializers.ModelSerializer):
    """Сериализатор для ингредиентов в рецепте.
    Отличается от сериализатора ингредиентов лишь полем количества"""
    id = serializers.PrimaryKeyRelatedField(
        queryset=Ingredient.objects.all(),
        source='ingredient.id',
    )

    name = serializers.CharField(
        read_only=True,
        source='ingredient.name',
    )

    measurement_unit = serializers.CharField(
        read_only=True,
        source='ingredient.measurement_unit',
    )

    class Meta:
        model = IngredientRecipe
        fields = (
            'id',
            'name',
            'measurement_unit',
            'amount',
        )


class RecipeSerializer(serializers.ModelSerializer):
    """Сериализатор для рецептов."""
    tags = TagSerializer(
        read_only=True,
        many=True,
    )

    author = AuthorSerializer(
        read_only=True,
    )

    ingredients = IngredientRecipeSerializer(
        read_only=True,
        many=True,
        source='recipe_ingredients',
    )

    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    name = serializers.CharField(required=True)
    image = Base64ImageField(required=True)
    text = serializers.CharField(required=True)
    cooking_time = serializers.IntegerField(min_value=1, max_value=1000)

    class Meta:
        model = Recipe
        exclude = ('pub_date',)

    def get_is_favorited(self, data):
        request = self.context.get('request')
        user = request.user
        if user.is_authenticated:
            return (
                FavoriteRecipe.objects.filter(
                    user=user, recipe=data,
                ).exists()
            )
        return False

    def get_is_in_shopping_cart(self, data):
        request = self.context.get('request')
        user = request.user
        if user.is_authenticated:
            return (
                ShoppingCart.objects.filter(user=user, recipe=data).exists()
            )
        return False

    def create(self, validated_data):
        request = self.context.get('request')

        user = User.objects.get(pk=request.user.pk)
        ingredients = request.data.get('ingredients')
        tags_id = request.data.get('tags')

        recipe = Recipe.objects.create(author=user, **validated_data)

        for ingredient in ingredients:
            current_ingredient = Ingredient.objects.get(
                id=ingredient.get('id')
            )
            IngredientRecipe.objects.create(
                ingredient=current_ingredient,
                recipe=recipe,
                amount=ingredient.get('amount')
            )

        for tag_id in tags_id:
            current_tag = Tag.objects.get(id=tag_id)
            TagRecipe.objects.create(
                tag=current_tag,
                recipe=recipe,
            )
        return recipe

    def update(self, instance, validated_data):
        request = self.context.get('request')

        ingredients = request.data.get('ingredients')
        tags_id = request.data.get('tags')

        if ingredients:
            IngredientRecipe.objects.filter(recipe=instance).delete()
            for ingredient in ingredients:
                current_ingredient, _ = Ingredient.objects.get_or_create(
                    id=ingredient.get('id'),
                )
                IngredientRecipe.objects.create(
                    ingredient=current_ingredient,
                    recipe=instance,
                    amount=ingredient.get('amount'),
                )

        if tags_id:
            TagRecipe.objects.filter(recipe=instance).delete()
            for tag_id in tags_id:
                current_tag = Tag.objects.get(id=tag_id)
                TagRecipe.objects.create(
                    tag=current_tag,
                    recipe=instance,
                )

        return super().update(instance, validated_data)

    def to_representation(self, instance):
        response = super(RecipeSerializer, self).to_representation(instance)
        if instance.image:
            response['image'] = instance.image.url
        return response


class RecipeMinimizedSerializer(serializers.ModelSerializer):
    """Сериализатор для рецептов с меньшим набором полей."""
    id = serializers.PrimaryKeyRelatedField(
        queryset=Recipe.objects.all(),
    )

    name = serializers.CharField(
        read_only=True,
    )

    image = Base64ImageField(required=True)

    cooking_time = serializers.CharField(
        read_only=True,
    )

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')
