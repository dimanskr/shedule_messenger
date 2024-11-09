from django.urls import path

from blog.apps import BlogConfig
from blog.views import ArticleListView, ArticleDetailView, ArticleCreateView, ArticleUpdateView, ArticleDeleteView

app_name = BlogConfig.name

urlpatterns = [
    path('articles/', ArticleListView.as_view(), name='articles'),
    path('articles/create/', ArticleCreateView.as_view(), name='article_create'),
    path('articles/<slug:slug>/', ArticleDetailView.as_view(), name='article_detail'),
    path('articles/<slug:slug>/edit', ArticleUpdateView.as_view(), name='article_update'),
    path('articles/<slug:slug>/delete', ArticleDeleteView.as_view(), name='article_delete'),
]