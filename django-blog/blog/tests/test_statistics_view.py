from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

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
