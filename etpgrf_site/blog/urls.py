from django.urls import path
from django.conf import settings
from . import views

app_name = 'blog' # Пространство имен для приложения blog

urlpatterns = [
    # Лента блога: /blog/
    path('', views.post_list, name='post_list'),
]

# Песочница для верстки: /blog/tmp/
# Добавляем ТОЛЬКО если DEBUG=True и ПЕРЕД post_detail
if settings.DEBUG:
    urlpatterns.append(path('tmp/', views.tmp_view, name='tmp'))

# Детальная страница поста: /blog/my-awesome-post/
# Этот маршрут должен быть последним, так как он перехватывает всё, что похоже на slug
urlpatterns.append(path('<slug:slug>/', views.post_detail, name='post_detail'))
