from django.contrib import admin

from recipes.models import IngredientRecipe, TagRecipe, Recipe, Tag, Ingredient


class TagInline(admin.TabularInline):
    model = TagRecipe


class IngredientInline(admin.TabularInline):
    model = IngredientRecipe


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    inlines = (
        TagInline,
    )
    list_display = ('name', 'color', 'slug')
    list_filter = ('name',)
    search_fields = ('name',)


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    inlines = (
        IngredientInline,
    )
    list_display = ('name', 'measurement_unit')
    list_filter = ('name',)
    search_fields = ('name',)


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    inlines = (
        TagInline, IngredientInline,
    )
    list_display = ('name', 'author', 'count_favorite')
    list_filter = ('name', 'author', 'tags')
    search_fields = ('name', 'author', 'tags')
    empty_value_display = '-пусто-'
    readonly_fields = ('count_favorite',)

    def count_favorite(self, obj):
        return obj.favorite_recipe.count()

    count_favorite.short_description = 'Добавили в избранное'
