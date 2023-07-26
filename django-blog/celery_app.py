import os
from celery import Celery
from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dj_blog.settings")

app = Celery('dj_blog')
app.config_from_object('django.conf:settings')
app.conf.broker_url = settings.CELERY_BROKER_URL
app.autodiscover_tasks()


app.conf.beat_schedule = {
    'publish-posts-every-minute': {
        'task': 'blog.tasks.publish_posts',
        'schedule': 60.0,
    },
}