from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap # Импортируем view для sitemap
from blog import views as blog_views
from blog.sitemaps import PostSitemap # Импортируем наш класс Sitemap

# Словарь с картами сайта
sitemaps = {
    'posts': PostSitemap,
}

urlpatterns = [
    path('adm-in/', admin.site.urls),
    path('', include('typograph.urls')),
    
    # Блог
    path('blog/', include('blog.urls')),
    
    # Sitemap.xml
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    
    # Статические страницы (ловушка в самом конце)
    path('<slug:slug>/', blog_views.page_detail, name='page_detail'),
]

# Для отдачи медиафайлов в режиме разработки
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
