from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, RegexValidator
from django.db import models


User = get_user_model()


class Tag(models.Model):
    """Модель тега."""
    objects = models.Manager()
    name = models.CharField(
        max_length=20, unique=True,
        verbose_name='Название',
    )

    color = models.CharField(
        max_length=7, unique=True,
        validators=[
            RegexValidator(
                '^#([a-fA-F0-9]{6}|[a-fA-F0-9]{3})$',
                message='Неверный HEX-код',
            )
        ],
        verbose_name='Цвет (например, #49B64E)',
    )

    slug = models.CharField(
        max_length=20, unique=True,
        verbose_name='Слаг',
    )

    class Meta:
        ordering = ('slug',)
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    """Модель ингредиента."""
    objects = models.Manager()
    name = models.CharField(
        max_length=64,
        verbose_name='Ингредиент',
    )

    measurement_unit = models.CharField(
        max_length=16,
        verbose_name='Единица измерения',
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return self.name


class Recipe(models.Model):
    """Модель рецепта."""
    objects = models.Manager()
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='recipes',
        verbose_name='Автор рецепта',
    )

    name = models.CharField(
        max_length=100,
        verbose_name='Название',
    )

    image = models.ImageField(
        upload_to='images/',
        verbose_name='Изображение рецепта',
    )

    text = models.TextField(
        verbose_name='Описание',
    )

    ingredients = models.ManyToManyField(
        Ingredient, through='IngredientRecipe', related_name='recipes',
        verbose_name='Ингредиенты',
    )

    tags = models.ManyToManyField(
        Tag, through='TagRecipe', related_name='recipes',
        verbose_name='Теги',
    )

    cooking_time = models.PositiveSmallIntegerField(
        default=1, validators=[MinValueValidator(1)],
        verbose_name='Время приготовления',
    )

    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации',
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class IngredientRecipe(models.Model):
    """Модель для свзяи рецепта и ингредиента."""
    objects = models.Manager()
    ingredient = models.ForeignKey(
        Ingredient, on_delete=models.CASCADE,
        related_name='recipe_ingredients',
    )

    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE,
        related_name='recipe_ingredients',
    )

    amount = models.PositiveSmallIntegerField(
        default=1, validators=[MinValueValidator(1)],
        verbose_name='Количество',
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['ingredient', 'recipe'],
                name='unique_ingredient_recipe',
            )
        ]
        verbose_name = 'Ингредиент рецепта'
        verbose_name_plural = 'Ингредиенты рецепта'

    def __str__(self):
        return f'{self.ingredient} для {self.recipe}'


class TagRecipe(models.Model):
    """Модель для связи рецепта и тега."""
    objects = models.Manager()
    tag = models.ForeignKey(
        Tag, on_delete=models.CASCADE,
    )

    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE,
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['tag', 'recipe'],
                name='unique_tag_recipe',
            )
        ]
        verbose_name = 'Тег рецепта'
        verbose_name_plural = 'Теги рецепта'

    def __str__(self):
        return f'{self.tag} для {self.recipe}'


class FavoriteRecipe(models.Model):
    """Модель избранных рецептов. Связывает пользователя и рецепт."""
    objects = models.Manager()
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='favorite_recipe',
    )
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name='favorite_recipe',
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_favorite_recipe',
            )
        ]
        verbose_name = 'Избранный рецепт'
        verbose_name_plural = 'Избранные рецепты'


class ShoppingCart(models.Model):
    """Модель списка покупок. Связывает пользователя и рецепт."""
    objects = models.Manager()
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='shopping_cart_item',
    )
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name='shopping_cart_item',
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_shopping_cart_item',
            )
        ]
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Списки покупок'
