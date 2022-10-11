from django.contrib.auth import get_user_model
from django.test import TestCase

from posts.models import Group, Post

User = get_user_model()

POST_STR_LENGTH: int = 15  # Количество символов метода __str__ в модели Post


class PostModelTest(TestCase):
    """Тестовый пост."""

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.user = User.objects.create_user(username='StasBasov')
        cls.post = Post.objects.create(
            author=cls.user,
            text='Длинный текст ' * POST_STR_LENGTH,
        )

    def test_models_have_correct_object_names(self):
        """Проверяем, что у модели Post корректно работает __str__."""
        post = PostModelTest.post
        expected_object_name = post.text[:POST_STR_LENGTH]
        self.assertEqual(
            expected_object_name,
            str(post),
            (
                'Метод __str__ модели Post должен выводить первые '
                f'{POST_STR_LENGTH} символов поста'
            )
        )

    def test_verbose_name(self):
        """verbose_name в полях модели Post совпадает с ожидаемым."""
        post = PostModelTest.post
        field_verboses = {
            'text': 'Текст',
            'pub_date': 'Дата создания',
            'author': 'Автор',
            'group': 'Группа',
        }
        for value, expected in field_verboses.items():
            with self.subTest(value=value):
                self.assertEqual(
                    post._meta.get_field(value).verbose_name,
                    expected,
                    f'Проверьте значение verbose_name поля {value}'
                )

    def test_help_text(self):
        """help_text в полях модели Post совпадает с ожидаемым."""
        post = PostModelTest.post
        field_help_texts = {
            'text': 'Введите текст поста',
            'group': 'Группа, к которой будет относиться пост',
        }
        for value, expected in field_help_texts.items():
            with self.subTest(value=value):
                self.assertEqual(
                    post._meta.get_field(value).help_text,
                    expected,
                    f'Проверьте значение help_texts поля {value}'
                )


class GroupModelTest(TestCase):
    """Тестовая группа."""

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='Тестовый слаг',
            description='Тестовое описание',
        )

    def test_models_have_correct_object_names(self):
        """Проверяем, что у модели Group корректно работает __str__."""
        group = GroupModelTest.group
        expected_object_name = group.title
        self.assertEqual(
            expected_object_name,
            str(group),
            'Метод __str__ модели Group должен выводить название группы'
        )

    def test_verbose_name(self):
        """verbose_name в полях модели Group совпадает с ожидаемым."""
        group = GroupModelTest.group
        field_verboses = {
            'title': 'Название группы',
            'slug': 'Слаг',
            'description': 'Описание',
        }
        for value, expected in field_verboses.items():
            with self.subTest(value=value):
                self.assertEqual(
                    group._meta.get_field(value).verbose_name,
                    expected,
                    f'Проверьте значение verbose_name поля {value}'
                )
