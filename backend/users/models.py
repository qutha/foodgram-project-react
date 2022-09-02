from django.contrib.auth.models import AbstractUser
from django.db import models


class AllFieldsRequiredUser(AbstractUser):
    """Модель пользователя."""
    email = models.EmailField(
        max_length=254,
        unique=True,
        verbose_name='Адрес электронной почты',
    )

    username = models.CharField(
        max_length=150,
        unique=True,
        verbose_name='Логин'
    )

    first_name = models.CharField(
        max_length=150,
        verbose_name='Имя',
    )

    last_name = models.CharField(
        max_length=150,
        verbose_name='Фамилия',
    )

    password = models.CharField(
        max_length=150,
        verbose_name='Пароль',
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = (
        'username', 'first_name', 'last_name', 'password',
    )

    class Meta:
        ordering = ['-id']
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)


class Follow(models.Model):
    """Модель подписок."""
    objects = models.Manager()
    user = models.ForeignKey(
        AllFieldsRequiredUser,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Подписчик',
    )

    author = models.ForeignKey(
        AllFieldsRequiredUser,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Пользователь, на которого подписываются',
    )

    class Meta:
        ordering = ['-id']
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'],
                name='unique_follow',
            ),
        ]
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'

    def __str__(self):
        return f'{self.user} подписан на {self.author}'
