from django.contrib.sitemaps import Sitemap
from .models import Post

class PostSitemap(Sitemap):
    changefreq = "weekly"  # Как часто меняются страницы
    priority = 0.9         # Приоритет (от 0.0 до 1.0)

    def items(self):
        """Возвращает все опубликованные посты и страницы."""
        return Post.objects.filter(is_published=True)

    def lastmod(self, obj):
        """Возвращает дату последнего изменения."""
        return obj.published_at # Или можно добавить поле updated_at
