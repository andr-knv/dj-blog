from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils import timezone
from tinymce.models import HTMLField


class Post(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField("Title", max_length=150)
    text = HTMLField()
    created_date = models.DateTimeField(default=timezone.now)
    publish_date = models.DateTimeField(blank=True, null=True)
    image = models.ImageField("Image", upload_to='post_image/')
    url = models.SlugField(max_length=150)
    is_published = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.title}'

    def get_absolute_url(self):
        return reverse("post_detail", kwargs={"slug": self.url})
