from django.shortcuts import get_object_or_404

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from recipes.filters import RecipeFilter
from recipes.models import (
    Tag, Ingredient, Recipe, FavoriteRecipe,
    ShoppingCart,
)
from recipes.permissions import IsAuthorOrReadOnly
from recipes.serializers import (
    TagSerializer, IngredientSerializer,
    RecipeSerializer, RecipeMinimizedSerializer,
)
from recipes.services import export_shopping_cart


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None
    permission_classes = [IsAuthenticatedOrReadOnly]


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = (SearchFilter,)
    search_fields = ('name',)


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    permission_classes = [IsAuthorOrReadOnly]
    filter_backends = (DjangoFilterBackend,)
    filter_class = RecipeFilter

    def get_serializer_class(self):
        if self.action in ('favorite', 'shopping_cart'):
            return RecipeMinimizedSerializer
        return RecipeSerializer

    @action(
        detail=True,
        methods=['POST', 'DELETE'],
        permission_classes=[IsAuthenticatedOrReadOnly],
    )
    def favorite(self, request, pk):
        user = request.user
        recipe = get_object_or_404(Recipe, pk=pk)

        if request.method == 'POST':
            favorite_recipe, created = FavoriteRecipe.objects.get_or_create(
                user=user, recipe=recipe,
            )
            if not created:
                return Response(
                    {'detail': 'Рецепт уже есть в избранном.'},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            serializer = self.get_serializer(favorite_recipe.recipe)
            return Response(data=serializer.data, status=status.HTTP_200_OK)

        elif request.method == 'DELETE':
            is_favorite_recipe_exists = FavoriteRecipe.objects.filter(
                user=user, recipe=recipe,
            ).exists()
            if not is_favorite_recipe_exists:
                return Response(
                    {'detail': 'Рецепт не был в избранном.'},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            FavoriteRecipe.objects.filter(
                user=user, recipe=recipe,
            ).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=True,
        methods=['POST', 'DELETE'],
        permission_classes=[IsAuthenticatedOrReadOnly],
    )
    def shopping_cart(self, request, pk):
        user = request.user
        recipe = get_object_or_404(Recipe, pk=pk)

        if request.method == 'POST':
            shopping_cart_item, created = ShoppingCart.objects.get_or_create(
                user=user, recipe=recipe,
            )
            if not created:
                return Response(
                    {'detail': 'Рецепт уже есть в списке покупок.'},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            serializer = self.get_serializer(shopping_cart_item.recipe)
            return Response(data=serializer.data, status=status.HTTP_200_OK)

        elif request.method == 'DELETE':
            is_favorite_recipe_exists = ShoppingCart.objects.filter(
                user=user, recipe=recipe,
            ).exists()
            if not is_favorite_recipe_exists:
                return Response(
                    {'detail': 'Рецепт не был в списке покупок.'},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            ShoppingCart.objects.filter(
                user=user, recipe=recipe,
            ).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=False,
        methods=['GET',],
        permission_classes=[IsAuthenticatedOrReadOnly],
    )
    def download_shopping_cart(self, request):
        try:
            return export_shopping_cart(request)
        except:
            return Response(
                {'detail': 'Извините, не получилось :(\nПовторите позднее.'},
                status=status.HTTP_400_BAD_REQUEST
            )
