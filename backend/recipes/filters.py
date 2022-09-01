from django_filters import CharFilter, ModelMultipleChoiceFilter
from django_filters.rest_framework import FilterSet, BooleanFilter

from recipes.models import Recipe, Tag


class RecipeFilter(FilterSet):
    author = CharFilter()
    name = CharFilter()

    tags = ModelMultipleChoiceFilter(
        queryset=Tag.objects.all(),
        field_name='tags__slug',
        to_field_name='slug',
    )

    is_favorite = BooleanFilter(
        field_name='is_favorite', method='filter',
    )
    is_in_shopping_cart = BooleanFilter(
        field_name='is_in_shopping_cart', method='filter',
    )

    def filter(self, queryset, name, value):
        if name == 'is_in_shopping_cart' and value:
            queryset = queryset.filter(
                shopping_cart_item__user=self.request.user
            )
        if name == 'is_favorited' and value:
            queryset = queryset.filter(
                favorite_recipe__user=self.request.user
            )
        return queryset

    class Meta:
        model = Recipe
        fields = (
            'author',
            'name',
            'tags',
            'is_favorite',
            'is_in_shopping_cart',
        )
