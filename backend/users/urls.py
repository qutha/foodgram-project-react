
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from users.views import AllFieldsRequiredUserViewSet

router_v1 = DefaultRouter()
router_v1.register('users', AllFieldsRequiredUserViewSet, basename='users')

subscriptions = AllFieldsRequiredUserViewSet.as_view({'get': 'subscriptions', })

urlpatterns = [
    path('users/subscriptions/', subscriptions, name='subscriptions'),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    path('', include(router_v1.urls)),
]
