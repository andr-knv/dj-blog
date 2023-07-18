from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Max, Count
from django.http import HttpResponseForbidden
from django.utils import timezone
from django.utils.text import slugify
from django.views.generic import ListView, DetailView, CreateView, UpdateView, TemplateView

from .forms import PostForm
from .models import Post


class PostsView(ListView):
    """Отображение всех постов"""
    model = Post
    queryset = Post.objects.select_related("author").order_by('-publish_date')


class PostDetailView(DetailView):
    """Полное отображение поста"""
    model = Post
    slug_field = "url"


class AuthorPosts(TemplateView):
    """Отображение всех постов автора"""
    template_name = "blog/user_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        author_name = self.kwargs['author_name']

        data = Post.objects.filter(
            author__username=author_name
        ).values(
            'author__username', 'url', 'title', 'publish_date'
        )
        latest = Post.objects.filter(author__username=author_name).latest('publish_date')

        context['posts'] = data
        context['latest'] = latest.publish_date
        print(latest)

        return context


class PostCreateView(LoginRequiredMixin, CreateView):
    """Форма для публикации поста"""
    model = Post
    template_name = 'blog/post_create.html'
    form_class = PostForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.publish_date = timezone.now()
        slug = slugify(f'{form.instance.title}-{timezone.now()}')
        form.instance.url = slug
        return super().form_valid(form)

    def handle_no_permission(self):
        return HttpResponseForbidden()


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Форма для редактирования поста"""
    model = Post
    template_name = "blog/post_update.html"
    form_class = PostForm
    slug_field = 'url'

    def test_func(self):
        post = self.get_object()
        return self.request.user.is_superuser or self.request.user == post.author

    def handle_no_permission(self):
        return HttpResponseForbidden()

    def form_valid(self, form):
        return super().form_valid(form)


class StatisticsView(TemplateView):
    template_name = "blog/stats.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        data = Post.objects.values(
            'author__username'
        ).annotate(num_posts=Count('author__username'),
                   last_publish_date=Max('publish_date'))
        context['authors_stats'] = data

        return context
