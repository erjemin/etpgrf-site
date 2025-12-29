from django.shortcuts import render
from django.http import HttpResponse
from etpgrf import Typographer

# Инициализируем типограф один раз (как рекомендовано в спеке)
# Можно вынести настройки в settings.py, но пока так
typo = Typographer(langs='ru', process_html=True, hanging_punctuation='both')

def index(request):
    return render(request, template_name='typograph/index.html')


def process_text(request):
    if request.method == 'POST':
        text = request.POST.get(key='text', default='')
        # Обрабатываем текст
        processed = typo.process(text)
        
        # Возвращаем только фрагмент для HTMX
        return render(request, template_name='typograph/result_fragment.html', context={'processed_text': processed})
    
    return HttpResponse(status=405)
