from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

from blog.models import Post


class TestStatisticsView(TestCase):
    def setUp(self) -> None:
        self.author1 = User.objects.create_user(username='author1', password='password')
        self.author2 = User.objects.create_user(username='author2', password='password')

        Post.objects.create(author=self.author1, title='Post 1 by Author 1', text='Test text 1')
        Post.objects.create(author=self.author1, title='Post 2 by Author 1', text='Test text 2')
        Post.objects.create(author=self.author2, title='Post 1 by Author 2', text='Test text 3')

    def test_statistics_view(self):
        """Тест подсчета количества статей и вывода последней даты"""
        url = reverse('stats')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        authors_stats = response.context['authors_stats']

        self.assertEqual(len(authors_stats), 2)

        for author in authors_stats:
            username = author['author__username']
            num_posts = author['num_posts']
            last_publish_date = author['last_publish_date']

            if username == 'author1':
                self.assertEqual(num_posts, 2)
                latest_post = Post.objects.filter(author__username=username).latest('publish_date')
                self.assertEqual(last_publish_date, latest_post.publish_date)
            elif username == 'author2':
                self.assertEqual(num_posts, 1)
                latest_post = Post.objects.filter(author__username=username).latest('publish_date')
                self.assertEqual(last_publish_date, latest_post.publish_date)


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
