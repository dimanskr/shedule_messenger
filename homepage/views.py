from django.views.generic import TemplateView

from blog.models import Article
from homepage.services import get_random_articles_from_cache
from mailing.models import Mailing, Client
from django.db.models import Q

class HomePageView(TemplateView):
    template_name = 'homepage/index.html'

    def get_context_data(self, **kwargs):
        random_blog_posts = get_random_articles_from_cache
        context_data = super().get_context_data(**kwargs)
        context_data['total_mailings'] = Mailing.objects.count()
        context_data['active_mailings'] = Mailing.objects.filter(~Q(status='completed') & Q(is_active=True)).count()
        context_data['unique_clients'] = Client.objects.values('email').distinct().count()
        context_data['random_blog_posts'] = random_blog_posts
        return context_data