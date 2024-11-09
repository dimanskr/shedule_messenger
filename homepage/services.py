from asyncio import timeout

from blog.models import Article
from django.core.cache import cache
from config.settings import CACHE_ENABLED, HOME_PAGE_CACHE_TIME


def get_random_articles_from_cache():
    """
    Получение статей на главную из кэша (если кэш пуст, то из БД)
    """
    if not CACHE_ENABLED:
        return Article.objects.filter(is_published=True).order_by('?')[:3]
    key = 'random_articles'
    articles = cache.get(key)
    if articles is not None:
        return articles
    articles = Article.objects.filter(is_published=True).order_by('?')[:3]
    cache.set(key, articles, timeout=HOME_PAGE_CACHE_TIME)
    return articles