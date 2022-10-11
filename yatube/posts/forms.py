from django import forms

from .models import Comment, Post


class PostForm(forms.ModelForm):
    """Форма добавляет пост.

    Пост содержит текст, картинку и название
    группы в которой пост публикуется.
    """

    class Meta:
        model = Post
        fields = ('text', 'group', 'image')
        help_texts = {
            'text': 'Текст поста',
            'group': 'Группа',
            'image': 'Картинка'
        }
        labels = {
            'text': 'Текст нового поста',
            'group': 'Группа, к которой будет относиться пост',
            'image': 'Картинка, которая будет добавлена к посту'
        }


class CommentForm(forms.ModelForm):
    """Форма добавляет комментарий к посту."""

    class Meta:
        model = Comment
        fields = ('text',)
        help_texts = {'text': 'Добавить комментарий'}
        labels = {'text': 'Текст комментария'}
