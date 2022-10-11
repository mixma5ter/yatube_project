from django.contrib.auth import get_user_model
from django.test import Client, TestCase

from http import HTTPStatus

# from posts.models import Group, Post

User = get_user_model()


class UsersURLTests(TestCase):
    """Тестовый пользователь."""

    def setUp(self):
        # Создаем неавторизованный клиент
        self.guest_client = Client()

        # Создаем авторизованый клиент
        self.user = User.objects.create_user(username='StasBasov')
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    # Проверяем доступность страниц для авторизованного пользователя
    def test_users_url_exists_for_authorized_user(self):
        """Проверка доступности страниц для авторизованного пользователя."""
        field_urls = {
            'logout': '/auth/logout/',
            # 'password_change': '/auth/password_change/',
            # 'password_change_done': '/auth/password_change/done/'
        }
        for value, expected in field_urls.items():
            response = self.authorized_client.get(expected)
            with self.subTest(value=value):
                self.assertEqual(
                    response.status_code,
                    HTTPStatus.OK,
                    f'Страница {value} не доступна'
                )

    # Проверяем доступность страниц для неавторизованного пользователя
    def test_users_url_exists_for_authorized_user(self):
        """Проверка доступности страниц для неавторизованного пользователя."""
        field_urls = {
            'signup': '/auth/signup/',
            'login': '/auth/login/',
            'password_reset': '/auth/password_reset/',
            'password_reset_done': '/auth/password_reset/done/',
            '/reset_token': '/auth/reset/<uidb64>/<token>/',
            'reset_done': '/auth/reset/done/'
        }
        for value, expected in field_urls.items():
            response = self.guest_client.get(expected)
            with self.subTest(value=value):
                self.assertEqual(
                    response.status_code,
                    HTTPStatus.OK,
                    f'Страница {value} не доступна'
                )
