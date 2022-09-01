from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(('users.urls', 'users'), namespace='users')),
    path('api/', include(('recipes.urls', 'recipes'), namespace='recipes')),
]


# from django.contrib import admin
# from django.urls import path, include
# from rest_framework.routers import DefaultRouter
#
# from recipes.views import TagViewSet, IngredientViewSet
# from users.views import CustomUserViewSet
#
# router_v1 = DefaultRouter()
# router_v1.register('users', CustomUserViewSet, basename='users')
# router_v1.register(r'tags', TagViewSet, basename='tags')
# router_v1.register(r'ingredients', IngredientViewSet, basename='tags')
#
# subscriptions = CustomUserViewSet.as_view({'get': 'subscriptions', })
#
# urlpatterns = [
#     path('admin/', admin.site.urls),
#
#     path('api/users/subscriptions/', subscriptions, name='subscriptions'),
#     path('api/', include('djoser.urls')),
#     path('api/auth/', include('djoser.urls.authtoken')),
#     path('api/', include(router_v1.urls)),
# ]
