from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from datetime import datetime, timedelta

from blog.models import Post

class TestAccess(TestCase):
    def setUp(self) -> None:
        self.admin = User.objects.create_superuser(username='admin', password='password')
        self.author = User.objects.create_user(username='author', password='password')
        self.user = User.objects.create_user(username='user', password='password')

        now = timezone.now()

        self.post = Post.objects.create(
            author=self.author,
            title=f"Test Post 1",
            text=f"Test Text 1",
            publish_date=now + timedelta(days=1),
            is_published=False,
            url='test-post',
        )

    def test_access(self):
        url = reverse('post_detail', args=[self.post.url])

        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

        self.client.login(username='user', password='password')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

        self.client.login(username='author', password='password')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        self.client.login(username='admin', password='password')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

