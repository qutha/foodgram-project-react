from django.urls import path, include
from rest_framework.routers import DefaultRouter

from recipes.views import TagViewSet, IngredientViewSet, RecipeViewSet

router_v1 = DefaultRouter()
router_v1.register('tags', TagViewSet, basename='tags')
router_v1.register('ingredients', IngredientViewSet, basename='tags')
router_v1.register('recipes', RecipeViewSet, basename='recipes')


urlpatterns = [
    path('', include(router_v1.urls)),
]
