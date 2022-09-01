from django.contrib import admin
from django.contrib.auth import get_user_model

from users.models import Follow

User = get_user_model()

@admin.register(User)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'username', 'first_name', 'last_name')
    list_filter = ('email', 'username')
    list_per_page = 10
    search_fields = ('email', 'search_fields')
    empty_value_display = '-пусто-'


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ('user', 'author')
    list_filter = ('user', 'author')
    list_per_page = 10
    search_fields = ('user', 'author')
    empty_value_display = '-пусто-'
