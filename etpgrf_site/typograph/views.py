from django.shortcuts import render
from django.http import HttpResponse
# Импортируем напрямую из пакета etpgrf, который лежит в корне проекта
from etpgrf.typograph import Typographer

def index(request):
    return render(request, template_name='typograph/index.html')

def process_text(request):
    if request.method == 'POST':
        text = request.POST.get(key='text', default='')
        
        # Собираем настройки из формы
        options = {
            # Выпадающие списки
            'langs': request.POST.get(key='langs', default='ru'),
            'hanging_punctuation': request.POST.get(key='hanging_punctuation', default='both'),
            'mode': request.POST.get(key='mode', default='mixed'),
            
            'process_html': True,
            
            # Чекбоксы
            'quotes': request.POST.get('quotes') == 'on',
            'layout': request.POST.get('layout') == 'on',
            'unbreakables': request.POST.get('unbreakables') == 'on',
            'hyphenation': request.POST.get('hyphenation') == 'on',
            'symbols': request.POST.get('symbols') == 'on',
        }
        
        if options['hanging_punctuation'] == 'none':
            options['hanging_punctuation'] = None

        # Создаем экземпляр типографа
        typo = Typographer(**options)
        
        # Обрабатываем текст
        processed = typo.process(text)
        
        # Возвращаем фрагмент с явным указанием аргументов
        return render(
            request, 
            template_name='typograph/result_fragment.html', 
            context={'processed_text': processed}
        )
    
    return HttpResponse(status=405)
