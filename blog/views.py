from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from pytils.translit import slugify
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin

from blog.forms import ArticleForm
from blog.models import Article
from config.settings import OBJECTS_ON_PAGE_COUNT


class ArticleListView(ListView):
    extra_context = {
        'title': 'Новости',
    }
    model = Article
    paginate_by = OBJECTS_ON_PAGE_COUNT
    context_object_name = "article_list"

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        user = self.request.user

        # Контент-менеджер может видеть все статьи
        if user.has_perm('blog.add_article') and user.has_perm('blog.change_article'):
            return queryset

        # Обычный пользователь видит только опубликованные статьи
        return queryset.filter(is_published=True)


class ArticleDetailView(DetailView):
    model = Article
    context_object_name = "article"

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.view_count += 1
        self.object.save()
        return self.object


class ArticleCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Article
    form_class = ArticleForm
    permission_required = ['blog.add_article']

    def form_valid(self, form):
        new_article = form.save(commit=False)
        new_article.slug = slugify(new_article.title)
        new_article.save()

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('blog:article_detail', kwargs={'slug': self.object.slug})


class ArticleUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Article
    form_class = ArticleForm
    permission_required = ['blog.change_article']

    def form_valid(self, form):
        new_article = form.save(commit=False)
        new_article.slug = slugify(new_article.title)
        new_article.save()

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('blog:article_detail', kwargs={'slug': self.object.slug})


class ArticleDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Article
    success_url = reverse_lazy('blog:articles')

    def test_func(self):
        return self.request.user.is_superuser

