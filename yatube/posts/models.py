from core.models import CreatedModel

from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

STR_LENGTH: int = 15


class Post(CreatedModel):
    """Модель поста сообщества."""

    text = models.TextField(
        verbose_name='Текст',
        help_text='Введите текст поста'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts',
        verbose_name='Автор'
    )
    group = models.ForeignKey(
        'Group',
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='posts',
        verbose_name='Группа',
        help_text='Группа, к которой будет относиться пост'
    )
    image = models.ImageField(
        'Image',
        upload_to='posts/',
        blank=True,
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'

    def __str__(self):
        return self.text[:STR_LENGTH]


class Group(models.Model):
    """Модель группы постов сообщества."""

    title = models.CharField(
        verbose_name='Название группы',
        max_length=200
    )
    slug = models.SlugField(
        unique=True,
        verbose_name='Слаг'
    )
    description = models.TextField(
        verbose_name='Описание',
    )

    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = "Группы"

    def __str__(self):
        return self.title[:STR_LENGTH]


class Comment(CreatedModel):
    """Модель комментария постов."""

    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Пост'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор комментария'
    )
    text = models.TextField(
        verbose_name='Текст комментария',
        help_text='Введите текст комментария'
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Комментарий'
        verbose_name_plural = "Комментарии"

    def __str__(self):
        return self.text[:STR_LENGTH]


class Follow(models.Model):
    """Модель подписки на авторов."""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Пользователь'  # Подписчик
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Автор'  # Подписки
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = "Подписки"

    def __str__(self):
        return self.author
