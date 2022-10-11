from django.test import Client, TestCase
from django.urls import reverse


class StaticViewsTests(TestCase):
    def setUp(self):
        """Создаем неавторизованый клиент"""
        self.guest_client = Client()

    def test_about_uses_correct_template(self):
        """Проверка шаблона для адреса главной страницы."""
        field_temp = {
            reverse('about:author'): 'about/author.html',
            reverse('about:tech'): 'about/tech.html'
        }
        for value, expected in field_temp.items():
            response = self.guest_client.get(value)
            with self.subTest(value=value):
                self.assertTemplateUsed(
                    response,
                    expected,
                    f'Проверьте шаблон страницы {value}'
                )
