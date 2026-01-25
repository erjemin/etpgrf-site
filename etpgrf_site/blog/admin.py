from django.contrib import admin
from .models import Post

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'post_type', 'is_published', 'published_at')
    list_filter = ('post_type', 'is_published', 'published_at')
    search_fields = ('title', 'content', 'slug')
    prepopulated_fields = {'slug': ('title',)} 
    date_hierarchy = 'published_at'
    
    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'post_type', 'is_published', 'published_at')
        }),
        ('Контент', {
            'fields': ('image', 'excerpt', 'content')
        }),
        ('SEO', {
            'fields': ('seo_title', 'seo_description', 'seo_keywords'),
            'classes': ('collapse',)
        }),
    )
