from django.test import TestCase

from http import HTTPStatus


class ViewTestClass(TestCase):
    def test_error_page(self):
        response = self.client.get('/nonexist-page/')
        # Проверяем, что статус ответа сервера - 404
        self.assertEqual(response.status_code, HTTPStatus.NotFound)
        # Проверяем, что используется шаблон core/404.html
        self.assertTemplateUsed(response, 'core/404.html')
