from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import Post

class StaticViewSitemap(Sitemap):
    """Карта сайта для статических страниц (главная и др.)."""
    priority = 1.0
    changefreq = "daily"

    def items(self):
        return ['index']

    def location(self, item):
        return reverse(item)

class PostSitemap(Sitemap):
    changefreq = "weekly"  # Как часто меняются страницы
    priority = 0.9         # Приоритет (от 0.0 до 1.0)

    def items(self):
        """Возвращает все опубликованные посты и страницы."""
        return Post.objects.filter(is_published=True)

    def lastmod(self, obj):
        """Возвращает дату последнего изменения."""
        return obj.updated_at # Используем дату обновления, а не публикации
