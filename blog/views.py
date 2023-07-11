from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.http import HttpResponseForbidden
from django.utils import timezone
from django.utils.text import slugify
from django.views.generic import ListView, DetailView, CreateView

from .models import Post


class PostsView(ListView):
    """Отображение всех постов"""
    model = Post
    queryset = Post.objects.select_related("author").order_by('-publish_date')


class PostDetailView(DetailView):
    """Полное отображение поста"""
    model = Post
    slug_field = "url"


class AuthorPostsListView(ListView):
    """Отображение всех постов автора"""
    model = Post
    template_name = "blog/user_detail.html"
    context_object_name = 'posts'

    def get_queryset(self):
        author_name = self.kwargs['author_name']

        return Post.objects.select_related(
            'author'
        ).filter(author__username=author_name).values("title", "url", "publish_date")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        author_name = self.kwargs['author_name']

        last_publish_date = Post.objects.select_related(
            'author'
        ).filter(author__username=author_name).values('publish_date').last()

        context['last_publish_date'] = last_publish_date['publish_date']
        context['author_name'] = author_name
        return context


class PostCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    """Форма для публикации поста"""
    model = Post
    template_name = 'blog/post_create.html'
    fields = ['title', 'text', 'image']

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.publish_date = timezone.now()

        slug = slugify(form.instance.title)
        unique_slug = slug
        counter = 1
        while Post.objects.filter(url=unique_slug).exists():
            unique_slug = f"{slug}-{counter}"
            counter += 1

        form.instance.url = unique_slug
        return super().form_valid(form)

    def test_func(self):
        return self.request.user.is_authenticated

    def handle_no_permission(self):
        return HttpResponseForbidden()
