from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from blog import views as blog_views # Импортируем views из приложения blog
from blog.models import PostType # Для использования в корневом urls.py

urlpatterns = [
    path('adm-in/', admin.site.urls),
    path('', include('typograph.urls')), # Основное приложение типографа

    # Блог
    path('blog/', include('blog.urls')),

    # Статические страницы (ловушка в самом конце, чтобы не перехватывать другие URL)
    # Исключаем слаги, которые могут конфликтовать с другими URL-ами
    # Например, 'admin', 'blog', 'static', 'media'
    path('<slug:slug>/', blog_views.page_detail, name='page_detail'),
]

# Для отдачи медиафайлов в режиме разработки
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
