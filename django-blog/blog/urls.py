from django.urls import path

from blog import views

urlpatterns = [
    path("", views.PostsView.as_view()),
    path("<slug:slug>/", views.PostDetailView.as_view(), name="post_detail"),
    path('author/<str:author_name>/', views.AuthorPosts.as_view(), name='user_detail'),
    path('post/create/', views.PostCreateView.as_view(), name='post_create'),
    path('post/<slug:slug>/update/', views.PostUpdateView.as_view(), name='post_update'),
    path('authors/stats/', views.StatisticsView.as_view(), name='stats'),
    
]
