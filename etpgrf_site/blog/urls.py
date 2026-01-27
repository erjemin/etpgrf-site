from django.urls import path
from . import views
from blog.models import PostType # Для использования в корневом urls.py

app_name = 'blog' # Пространство имен для приложения blog

urlpatterns = [
    # Лента блога: /blog/
    path('', views.post_list, name='post_list'),
    
    # Песочница для верстки: /blog/tmp/
    path('tmp/', views.tmp_view, name='tmp'),
    
    # Детальная страница поста: /blog/my-awesome-post/
    path('<slug:slug>/', views.post_detail, name='post_detail'),
]
