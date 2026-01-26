from django.db import models
from django.utils import timezone
from django.urls import reverse

class PostType(models.TextChoices):
    BLOG = 'B', 'Пост в блог'
    PAGE = 'P', 'Страница'

class Post(models.Model):
    """
    Модель для постов блога и статических страниц.
    """
    title = models.CharField(
        verbose_name="Заголовок",
        max_length=255,
        help_text="Основной заголовок (H1). Обязательно для заполнения."
    )
    slug = models.SlugField(
        verbose_name="URL (slug)",
        max_length=255, 
        unique=True, 
        help_text="Уникальная часть адреса. Используйте латиницу, цифры и дефис. Например: my-new-post"
    )
    
    post_type = models.CharField(
        verbose_name="Тип публикации",
        max_length=1,
        choices=PostType.choices,
        default=PostType.BLOG,
        db_index=True,
        help_text="Страница доступна по адресу /slug/, Пост — по адресу /blog/slug/"
    )
    
    is_published = models.BooleanField(
        verbose_name="Опубликовано",
        default=True,
        db_index=True,
        help_text="Снимите галочку, чтобы скрыть публикацию (черновик)."
    )
    published_at = models.DateTimeField(
        verbose_name="Дата публикации",
        default=timezone.now,
        db_index=True,
        help_text="Дата, которая будет отображаться в блоге. Можно запланировать на будущее."
    )
    
    content = models.TextField(
        verbose_name="Контент",
        help_text="Основной текст публикации. Поддерживает HTML."
    )
    excerpt = models.TextField(
        verbose_name="Краткое описание (тизер)",
        blank=True, 
        help_text="Отображается в списке постов. Если оставить пустым, будет взято начало контента."
    )
    
    image = models.ImageField(
        verbose_name="Обложка",
        upload_to='blog/', 
        blank=True, 
        null=True,
        help_text="Изображение для превью в ленте и Open Graph (соцсети)."
    )
    
    # SEO
    seo_title = models.CharField(
        verbose_name="SEO Title",
        max_length=255, 
        blank=True,
        help_text="Заголовок для поисковиков (<tt>&lt;title&gt;</tt>). Если пусто, используется основной заголовок."
    )
    seo_description = models.TextField(
        verbose_name="SEO Description",
        blank=True,
        help_text="Описание для поисковиков (meta description). Рекомендуется 150-160 символов."
    )
    seo_keywords = models.CharField(
        verbose_name="SEO Keywords",
        max_length=255, 
        blank=True,
        help_text="Ключевые слова через запятую (meta keywords). Сейчас почти не используется поисковиками,"
                  "но может пригодиться."
    )

    class Meta:
        verbose_name = "Публикация"
        verbose_name_plural = "Публикации"
        ordering = ['-published_at']
        indexes = [
            # Индекс для быстрого поиска и сортировки постов блога
            models.Index(fields=['post_type', 'is_published', '-published_at'], name='blog_post_idx'),
            # Индекс для быстрых страниц (если post_type='P')
            models.Index(fields=['post_type', 'slug'], name='blog_page_slug_idx'),
        ]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        if self.post_type == PostType.PAGE:
            return reverse('page_detail', kwargs={'slug': self.slug})
        return reverse('post_detail', kwargs={'slug': self.slug})
