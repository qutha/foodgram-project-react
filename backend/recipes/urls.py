from django.urls import path, include
from rest_framework.routers import DefaultRouter

from recipes.views import TagViewSet, IngredientViewSet, RecipeViewSet

router_v1 = DefaultRouter()
router_v1.register(r'tags', TagViewSet, basename='tags')
router_v1.register(r'ingredients', IngredientViewSet, basename='tags')
router_v1.register(r'recipes', RecipeViewSet, basename='recipes')


urlpatterns = [
    path('', include(router_v1.urls)),
]
