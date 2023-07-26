from django.utils import timezone
from celery import shared_task
from .models import Post

@shared_task
def publish_posts():
    now = timezone.now()
    unpublished_posts = Post.objects.filter(is_published=False, publish_date__lte=now)
    for post in unpublished_posts:
        post.is_published = True
        post.save()