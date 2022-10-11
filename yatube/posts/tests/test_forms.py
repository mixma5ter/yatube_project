import shutil
import tempfile

from django.core.files.uploadedfile import SimpleUploadedFile

from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import Client, TestCase, override_settings
from django.urls import reverse

from posts.forms import PostForm
from posts.models import Comment, Group, Post

User = get_user_model()

# Для сохранения media-файлов в тестах будет использоваться
# временная папка TEMP_MEDIA_ROOT
TEMP_MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)

SMALL_GIF = (
    b'\x47\x49\x46\x38\x39\x61\x02\x00'
    b'\x01\x00\x80\x00\x00\x00\x00\x00'
    b'\xFF\xFF\xFF\x21\xF9\x04\x00\x00'
    b'\x00\x00\x00\x2C\x00\x00\x00\x00'
    b'\x02\x00\x01\x00\x00\x02\x02\x0C'
    b'\x0A\x00\x3B'
)


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class PostCreateFormTests(TestCase):
    """Проверка постов."""

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
        cls.image = SimpleUploadedFile(
            name='small.gif',
            content=SMALL_GIF,
            content_type='small/gif'
        )
        cls.form = PostForm()

    @classmethod
    def tearDownClass(cls):
        """Удаляет временную директорию и всё её содержимое"""
        super().tearDownClass()
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)

    def setUp(self):
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_create_post(self):
        """Валидная форма создает запись в Post."""
        # Подсчитаем количество записей в Post
        posts_count = Post.objects.count()
        form_data = {
            'author': self.user.username,
            'text': 'Новый тестовый текст',
            'group': self.group.id,
            'image': self.image
        }
        # Отправляем POST-запрос
        response = self.authorized_client.post(
            reverse('posts:post_create'),
            data=form_data,
            follow=True
        )
        # Проверяем, сработал ли редирект
        self.assertRedirects(
            response,
            reverse('posts:profile', kwargs={'username': self.user.username})
        )
        # Проверяем, увеличилось ли число постов
        self.assertEqual(Post.objects.count(), posts_count + 1)
        # Проверяем, что запись создалась
        last_post = Post.objects.first()
        self.assertEqual(last_post.author.username, form_data['author'])
        self.assertEqual(last_post.group.id, form_data['group'])
        self.assertEqual(last_post.text, form_data['text'])
        # self.assertEqual(last_post.image, form_data['image'])
        # так проверить не удалось
        self.assertTrue(
            Post.objects.filter(
                image='posts/small.gif'
            ).first()
        )

    def test_edit_post(self):
        """Валидная форма редактирует запись в Post."""
        # Подсчитаем количество записей в Post
        posts_count = Post.objects.count()
        form_data = {
            'author': self.user.username,
            'text': 'Измененный тестовый текст',
            'group': self.group.id,
        }
        # Отправляем POST-запрос
        response = self.authorized_client.post(
            reverse('posts:post_edit', kwargs={'post_id': self.post.id}),
            data=form_data,
            follow=True
        )
        # Проверяем, сработал ли редирект
        self.assertRedirects(
            response,
            reverse('posts:post_detail', kwargs={'post_id': self.post.id})
        )
        # Проверяем, что число постов не увеличилось
        self.assertEqual(Post.objects.count(), posts_count)
        # Проверяем, что запись изменилась
        last_post = Post.objects.get(id=self.post.id)
        self.assertEqual(last_post.author.username, form_data['author'])
        self.assertEqual(last_post.group.id, form_data['group'])
        self.assertEqual(last_post.text, form_data['text'])

    def test_title_label(self):
        """Проверяет метки полей формы"""
        text_label = self.form.fields['text'].label
        group_label = self.form.fields['group'].label
        self.assertEqual(text_label, 'Текст нового поста')
        self.assertEqual(
            group_label,
            'Группа, к которой будет относиться пост'
        )

    def test_title_help_text(self):
        """Проверяет тексты подсказок"""
        text_help_text = self.form.fields['text'].help_text
        group_help_text = self.form.fields['group'].help_text
        self.assertEqual(text_help_text, 'Текст поста')
        self.assertEqual(group_help_text, 'Группа')


class CommentTest(TestCase):
    """Проверка комментариев."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='StasBasov')
        cls.post = Post.objects.create(
            author=cls.user,
            text='Тестовый текст',
        )
        cls.comment = Comment.objects.create(
            post=cls.post,
            author=cls.user,
            text='Тестовый комментарий'
        )

    def setUp(self):
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_comment_appear(self):
        """Проверяет, что комментарий появился под постом."""
        response = self.authorized_client.get(
            reverse('posts:post_detail', kwargs={'post_id': self.post.id})
        )
        comment = response.context['comments'][0]
        self.assertEqual(comment.text, self.comment.text)
