from django.contrib.auth import get_user_model
from django.test import Client, TestCase

from http import HTTPStatus

from posts.models import Group, Post

User = get_user_model()


class PostsURLTests(TestCase):
    """Тестовый пост и группа."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='StasBasov')
        cls.group = Group.objects.create(
            title='Тестовое название группы',
            slug='test-slug',
            description='Тестовое описание',
        )
        cls.post = Post.objects.create(
            text='Тестовый текст',
            author=cls.user,
            group=cls.group
        )

    def setUp(self):
        # Создаем неавторизованный клиент
        self.guest_client = Client()

        # Создаем авторизованый клиент
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    # Проверяем общедоступные страницы
    def test_posts_url_exists_for_unauthorized_user(self):
        """Проверка доступности страниц для неавторизованного пользователя."""
        field_urls = {
            'index': '/',
            'group_list': f'/group/{self.group.slug}/',
            'profile': f'/profile/{self.user}/',
            'post_detail': f'/posts/{self.post.pk}/'
        }
        for value, expected in field_urls.items():
            response = self.guest_client.get(expected)
            with self.subTest(value=value):
                self.assertEqual(
                    response.status_code,
                    HTTPStatus.OK,
                    f'Страница {value} не доступна'
                )

    # Проверяем доступность страниц для авторизованного пользователя
    def test_create_url_exists_for_authorized_user(self):
        """Проверка доступности страниц для авторизованного пользователя."""
        field_urls = {
            'post_create': '/create/',
            'post_edit': f'/posts/{self.post.pk}/edit/'
        }
        for value, expected in field_urls.items():
            response = self.authorized_client.get(expected)
            with self.subTest(value=value):
                self.assertEqual(
                    response.status_code,
                    HTTPStatus.OK,
                    f'Страница {value} не доступна'
                )

    # Проверяем что отсутствующая страница возвращает ошибку 404
    def test_unexiting_page_list_url_unexists_at_desired_location(self):
        """Страница /unexiting_page/ не доступна никакому пользователю."""
        response = self.guest_client.get('/unexiting_page/')
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    # Проверяем редиректы для неавторизованного пользователя
    def test_posts_url_redirect_anonymous_on_admin_login(self):
        """Перенаправляет анонимного пользователя на страницу логина."""
        field_urls = {
            '/create/': '/auth/login/?next=/create/',
            f'/posts/{self.post.pk}/edit/':
                f'/auth/login/?next=/posts/{self.post.pk}/edit/'
        }
        for value, expected in field_urls.items():
            response = self.guest_client.get(value)
            with self.subTest(value=value):
                self.assertRedirects(response, expected)
