from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.core.paginator import Paginator
from .models import Post, PostType


def post_list(request):
    """
    Отображает список опубликованных постов блога с пагинацией.
    """
    # Фильтруем только посты блога, опубликованные и с датой публикации не позднее текущего момента
    posts_queryset = Post.objects.filter(
        post_type=PostType.BLOG,
        is_published=True,
        published_at__lte=timezone.now()
    ).order_by('-published_at') # Сортируем по дате публикации (от новых к старым)
    
    # Настраиваем пагинацию: 10 постов на страницу
    paginator = Paginator(posts_queryset, 10)
    page_number = request.GET.get('page') # Получаем номер страницы из GET-параметра
    page_obj = paginator.get_page(page_number) # Получаем объект страницы
    
    return render(request, 'blog/post_list.html', {'page_obj': page_obj})


def post_detail(request, slug):
    """
    Отображает детальную страницу конкретного поста блога.
    """
    # Ищем пост по слагу, типу 'BLOG', опубликованный и с датой публикации не позднее текущего момента
    post = get_object_or_404(
        Post, 
        slug=slug, 
        post_type=PostType.BLOG,
        is_published=True,
        published_at__lte=timezone.now()
    )
    return render(request, 'blog/post_detail.html', {'post': post})


def page_detail(request, slug):
    """
    Отображает детальную страницу статической страницы (например, /privacy-policy/).
    """
    # Ищем страницу по слагу, типу 'PAGE' и опубликованную
    page = get_object_or_404(
        Post, 
        slug=slug, 
        post_type=PostType.PAGE,
        is_published=True
    )
    return render(request, 'blog/page_detail.html', {'page': page})


def tmp_view(request):
    """
    Временная страница для верстки постов.
    Доступна только в DEBUG режиме (или можно оставить, если не мешает).
    """
    return render(request, 'blog/tmp.html')
