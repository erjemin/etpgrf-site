from django.contrib import admin
from django.utils.html import format_html
import html
from .models import Post

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('clean_title', 'post_type', 'is_published', 'published_at', 'updated_at')
    list_filter = ('post_type', 'is_published', 'published_at')
    search_fields = ('title', 'content', 'slug')
    prepopulated_fields = {'slug': ('title',)} 
    date_hierarchy = 'published_at'
    readonly_fields = ('updated_at',)
    
    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'post_type', 'is_published', 'published_at', 'updated_at')
        }),
        ('Контент', {
            'fields': ('image', 'excerpt', 'content')
        }),
        ('SEO', {
            'fields': ('seo_title', 'seo_description', 'seo_keywords'),
            'classes': ('collapse',)
        }),
    )

    @admin.display(description='Заголовок', ordering='title')
    def clean_title(self, obj):
        """Отображает заголовок без HTML-сущностей (&nbsp; -> пробел)."""
        return html.unescape(obj.title)
