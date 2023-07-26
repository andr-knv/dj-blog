from datetime import datetime, timedelta

from django.contrib.auth.models import User
from django.utils import timezone
from django.test import TestCase

from blog.models import Post
from blog.tasks import PostPublisher


class PostPublisherTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        now = timezone.now()
        self.unpublished_posts = []
        for i in range(3):
            post = Post.objects.create(
                author=self.user,
                title=f"Test Post {i}",
                text=f"Test Text {i}",
                publish_date=now - timedelta(days=i),
                is_published=False
            )
            self.unpublished_posts.append(post)


    def test_posts_are_in_db(self):
        posts = Post.objects.all()
        for post in posts:
            self.assertFalse(post.is_published)

    def test_select_posts(self):
        selected_posts = PostPublisher.select_posts()
        self.assertQuerysetEqual(selected_posts, self.unpublished_posts)

    def test_publish(self):
        for p in self.unpublished_posts:
            PostPublisher.publish_post(p)
        posts = Post.objects.all()

        for post in posts:
            self.assertTrue(post.is_published)
