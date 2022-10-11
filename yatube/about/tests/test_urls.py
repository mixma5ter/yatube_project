from django.test import Client, TestCase

from http import HTTPStatus


class StaticURLTests(TestCase):
    def setUp(self):
        """Создаем неавторизованый клиент"""
        self.guest_client = Client()

    def test_about_url_exists_at_desired_location(self):
        """Проверка доступности статических страниц."""
        field_urls = {
            'author': '/about/author/',
            'tech': '/about/tech/'
        }
        for value, expected in field_urls.items():
            response = self.guest_client.get(expected)
            with self.subTest(value=value):
                self.assertEqual(
                    response.status_code,
                    HTTPStatus.OK,
                    f'Страница {value} не доступна'
                )
