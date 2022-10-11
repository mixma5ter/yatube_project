from django import forms
from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.test import Client, TestCase
from django.urls import reverse

from posts.models import Group, Follow, Post
from posts.forms import PostForm

User = get_user_model()

POSTS_ON_PAGE_1 = 10
POSTS_ON_PAGE_2 = 3
POSTS_TOTAL = POSTS_ON_PAGE_1 + POSTS_ON_PAGE_2


class PostViewsTest(TestCase):
    """Тестовый пост и группы."""

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.user = User.objects.create_user(username='StasBasov')
        # Создаем группы
        cls.group = Group.objects.create(
            title='Тестовое название группы',
            slug='test-slug',
            description='Тестовое описание',
        )
        cls.group_2 = Group.objects.create(
            title='Тестовое название группы 2',
            slug='test-slug-2',
            description='Тестовое описание 2',
        )
        # Создаем посты
        cls.post = Post.objects.create(
            text='Тестовый текст',
            author=cls.user,
            group=cls.group
        )

    def setUp(self):
        # Создаем авторизованый клиент
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_pages_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        cache.clear()
        # Собираем в словарь пары "имя_html_шаблона: reverse(name)"
        templates_page_names = {
            reverse('posts:index'):
                'posts/index.html',
            reverse('posts:group_list', kwargs={'slug': self.group.slug}):
                'posts/group_list.html',
            reverse('posts:profile', kwargs={'username': self.user}):
                'posts/profile.html',
            reverse('posts:post_detail', kwargs={'post_id': self.post.id}):
                'posts/post_detail.html',
            reverse('posts:post_create'):
                'posts/create_post.html',
            reverse('posts:post_edit', kwargs={'post_id': self.post.id}):
                'posts/create_post.html',
        }
        # Проверяем, что при обращении к name
        # вызывается соответствующий HTML-шаблон
        for reverse_name, template in templates_page_names.items():
            with self.subTest(template=template):
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)

    def test_index_page_show_correct_context(self):
        """Шаблон главной страницы сформирован с правильным контекстом."""
        cache.clear()
        response = self.authorized_client.get(reverse('posts:index'))
        first_object = response.context['page_obj'][0]
        response_context = {
            self.user: first_object.author,
            self.post.text: first_object.text,
            self.post.id: first_object.id,
            self.group: first_object.group
        }
        for test_name, response_name in response_context.items():
            with self.subTest(test_name=test_name):
                self.assertEqual(response_name, test_name)

    def test_group_list_show_correct_context(self):
        """Шаблон group_list сформирован с правильным контекстом."""
        response = self.authorized_client.get(reverse(
            'posts:group_list', kwargs={'slug': self.group.slug}))
        first_object = response.context['page_obj'][0]
        response_context = {
            self.user.username: first_object.author.username,
            self.post.text: first_object.text,
            self.post.id: first_object.id,
            self.group: first_object.group
        }
        for test_name, response_name in response_context.items():
            with self.subTest(test_name=test_name):
                self.assertEqual(response_name, test_name)

    def test_profile_show_correct_context(self):
        """Шаблон profile сформирован с правильным контекстом."""
        response = self.authorized_client.get(reverse(
            'posts:profile', kwargs={'username': self.user.username}))
        first_object = response.context['page_obj'][0]
        response_context = {
            self.user: first_object.author,
            self.post.text: first_object.text,
            self.post.id: first_object.id,
            self.group: first_object.group
        }
        for test_name, response_name in response_context.items():
            with self.subTest(test_name=test_name):
                self.assertEqual(response_name, test_name)

    def test_post_detail_page_show_correct_context(self):
        """Шаблон post_detail сформирован с правильным контекстом."""
        response = (self.authorized_client.get(reverse(
            'posts:post_detail', kwargs={'post_id': self.post.id})))
        first_object = response.context['post']
        response_context = {
            self.user: first_object.author,
            self.post.text: first_object.text,
            self.post.id: first_object.id,
            self.group: first_object.group
        }
        for test_name, response_name in response_context.items():
            with self.subTest(test_name=test_name):
                self.assertEqual(response_name, test_name)

    def test_post_create_page_show_correct_context(self):
        """Шаблон post_create сформирован с правильным контекстом."""
        response = self.authorized_client.get(reverse('posts:post_create'))
        form_fields = {
            # При создании формы поля модели типа TextField
            # преобразуются в CharField с виджетом forms.Textarea
            'text': forms.fields.CharField,
            'group': forms.fields.ChoiceField
        }

        # Проверяем, что типы полей формы в словаре context
        # соответствуют ожиданиям
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context.get('form').fields.get(value)
                # Проверяет, что поле формы является экземпляром
                # указанного класса
                self.assertIsInstance(form_field, expected)
        self.assertIsInstance(response.context.get('form'), PostForm)
        self.assertTrue('is_edit' not in response.context)

    def test_post_edit_page_show_correct_context(self):
        """Шаблон post_edit сформирован с правильным контекстом."""
        response = (self.authorized_client.get(reverse(
            'posts:post_edit', kwargs={'post_id': self.post.id})))
        form_fields = {
            # При создании формы поля модели типа TextField
            # преобразуются в CharField с виджетом forms.Textarea
            'text': forms.fields.CharField,
            'group': forms.fields.ChoiceField
        }

        # Проверяем, что типы полей формы в словаре context
        # соответствуют ожиданиям
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context.get('form').fields.get(value)
                self.assertIsInstance(form_field, expected)
        self.assertIsInstance(response.context.get('form'), PostForm)
        self.assertTrue('is_edit' in response.context)

    def test_post_create_appears_on_correct_pages(self):
        """
        При создании поста он должен появляется на главной странице,
        на странице выбранной группы и в профиле пользователя.
        """
        cache.clear()
        pages = [
            reverse('posts:index'),
            reverse('posts:group_list', kwargs={'slug': self.group.slug}),
            reverse('posts:profile', kwargs={'username': self.user})
        ]
        for page in pages:
            with self.subTest(page=page):
                response = self.authorized_client.get(page)
                self.assertIn(self.post, response.context['page_obj'])

    def test_post_not_contain_in_wrong_group(self):
        """При создании поста он не появляется в другой группе."""
        # Создаем пост в второй группе
        Post.objects.create(
            text='Тестовый текст',
            author=self.user,
            group=self.group_2
        )
        response = self.authorized_client.get(
            reverse('posts:group_list', kwargs={'slug': self.group_2.slug})
        )
        self.assertNotIn(self.post, response.context['page_obj'])

    def test_index_cache(self):
        """Проверка работы кэша на главной странице."""
        # Получаем текущее количество постов
        posts = self.authorized_client.get(reverse('posts:index')).content
        # Создаем новый пост
        Post.objects.create(
            text='Тестовый текст нового поста',
            author=self.user,
        )
        # Запрашиваем страницу с постами и проверяем, что там нет нового поста
        posts_with_cache = self.authorized_client.get(
            reverse('posts:index')).content
        self.assertEqual(posts, posts_with_cache)
        # Очищаем кеш
        cache.clear()
        # Запрашиваем страницу с постами и проверяем, что там появился пост
        posts_without_cache = self.authorized_client.get(
            reverse('posts:index')).content
        self.assertNotEqual(posts, posts_without_cache)


class PaginatorViewsTest(TestCase):
    """Тест пагинатора."""

    def setUp(self):
        self.user = User.objects.create_user(username='StasBasov')
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)
        self.group = Group.objects.create(
            title='Тестовый заголовок группы',
            slug='Something'
        )
        for i in range(POSTS_TOTAL):
            Post.objects.create(
                author=self.user,
                text=f'Тестовый текст {i}',
                group=self.group
            )

    def test_pages_contain_correct_record_number(self):
        """Тестируем пагинатор первой и второй страниц."""
        cache.clear()
        fields = (
            reverse('posts:index'),
            reverse('posts:group_list', kwargs={'slug': self.group.slug}),
            reverse('posts:profile', kwargs={'username': self.user.username})
        )
        for field in fields:
            response_1 = self.client.get(field)
            response_2 = self.client.get(field, data={'page': 2})
            with self.subTest(value=field):
                self.assertEqual(
                    len(response_1.context['page_obj']),
                    POSTS_ON_PAGE_1
                )
                self.assertEqual(
                    len(response_2.context['page_obj']),
                    POSTS_ON_PAGE_2
                )


class FollowerTest(TestCase):
    """Тест подписок."""

    def setUp(self):
        cache.clear()
        self.user = User.objects.create_user(username='StasBasov')
        self.post = Post.objects.create(
            author=self.user,
            text='Тестовый текст',
        )
        self.follower = User.objects.create_user(username='follower')
        self.follow_client = Client()
        self.follow_client.force_login(self.follower)

    def test_follower_to_author(self):
        """Проверка подписки и отписки на авторов."""
        self.follow_client.get(
            reverse('posts:profile_follow', kwargs={'username': self.user}))
        follow = Follow.objects.filter(user=self.follower,
                                       author=self.user).exists()
        self.assertTrue(follow)
        self.follow_client.get(
            reverse('posts:profile_unfollow', kwargs={'username': self.user})
        )
        follow = Follow.objects.filter(user=self.follower,
                                       author=self.user).exists()
        self.assertEqual(follow, False)
