from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from blog.models import Post


class TestCreateUpdateViews(TestCase):
    def setUp(self) -> None:
        self.admin = User.objects.create_superuser(username='admin', password='password')
        self.author = User.objects.create_user(username='author', password='password')
        self.user = User.objects.create_user(username='user', password='password')

        self.post = Post.objects.create(
            author=self.author,
            title='Test Post',
            text='Test text.',
            image='test_image.jpg',
            url='test-post',
        )

    def test_post_update_view(self):
        """Тест доступа к post_update"""
        url = reverse('post_update', args=[self.post.url])

        # Неавторизованный пользователь
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

        # Авторизованный пользователь, не являющийся автором статьи
        self.client.login(username='user', password='password')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

        # Автор статьи
        self.client.login(username='author', password='password')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        # Админ
        self.client.login(username='admin', password='password')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_post_create_view(self):
        """Тест доступа к post_create"""
        url = reverse('post_create')

        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

        self.client.login(username='user', password='password')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        self.client.login(username='admin', password='password')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_editing_post(self):
        """Тест редактирования поста"""
        url = reverse('post_update', args=[self.post.url])

        self.client.login(username='author', password='password')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        updated_post_data = {
            'title': 'Updated Test Post',
            'text': 'Updated text.',
        }

        response = self.client.post(url, data=updated_post_data)
        self.assertEqual(response.status_code, 302)

        updated_post = Post.objects.get(pk=self.post.pk)
        self.assertEqual(updated_post.title, 'Updated Test Post')
        self.assertEqual(updated_post.text, 'Updated text.')
