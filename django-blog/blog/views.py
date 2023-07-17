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


# TODO: tinymce в шаблоне
# TODO: Черновик
# TODO: Авторизация

