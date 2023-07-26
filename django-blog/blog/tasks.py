from django.utils import timezone
from celery import shared_task
from .models import Post


class PostPublisher:
    @classmethod
    def select_posts(cls):
        now = timezone.now()
        return Post.objects.filter(is_published=False, publish_date__lte=now).order_by(
            '-publish_date')

    @classmethod
    def publish_post(cls, post):
        post.is_published = True
        post.save()


@shared_task
def publish_posts():
    unpublished_posts = PostPublisher.select_posts()
    for post in unpublished_posts:
        PostPublisher.publish_post(post)
