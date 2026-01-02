from django.shortcuts import render
from django.http import HttpResponse
from etpgrf.typograph import Typographer
from etpgrf.layout import LayoutProcessor
from etpgrf.hyphenation import Hyphenator

def index(request):
    return render(request, template_name='typograph/index.html')

def process_text(request):
    if request.method == 'POST':
        text = request.POST.get(key='text', default='')
        
        # 1. Читаем базовые настройки
        langs = request.POST.get(key='langs', default='ru')
        
        # 2. Собираем LayoutProcessor
        layout_enabled = request.POST.get('layout') == 'on'
        layout_option = False
        if layout_enabled:
            process_units = request.POST.get('layout_units') == 'on'
            if process_units:
                custom_units = request.POST.get('layout_units_custom', '').strip()
                if custom_units:
                    process_units = custom_units.split()
            
            layout_option = LayoutProcessor(
                langs=langs,
                process_initials_and_acronyms=request.POST.get('layout_initials') == 'on',
                process_units=process_units
            )
            
        # 3. Собираем Hyphenator
        hyphenation_enabled = request.POST.get('hyphenation') == 'on'
        hyphenation_option = False
        if hyphenation_enabled:
            max_len = request.POST.get('hyphenation_len', '15')
            try:
                max_len = int(max_len)
            except (ValueError, TypeError):
                max_len = 15 # Дефолтное значение, если пришло что-то не то
            
            hyphenation_option = Hyphenator(
                langs=langs,
                max_unhyphenated_len=max_len
            )

        # 4. Читаем Sanitizer
        sanitizer_val = request.POST.get('sanitizer', '')
        sanitizer_option = None
        if sanitizer_val:
            sanitizer_option = sanitizer_val

        # 5. Собираем общие опции
        options = {
            'langs': langs,
            'process_html': True,
            
            'quotes': request.POST.get('quotes') == 'on',
            'layout': layout_option,
            'unbreakables': request.POST.get('unbreakables') == 'on',
            'hyphenation': hyphenation_option,
            'symbols': request.POST.get('symbols') == 'on',
            
            'hanging_punctuation': request.POST.get(key='hanging_punctuation', default='none'),
            'mode': request.POST.get(key='mode', default='mixed'),
            
            'sanitizer': sanitizer_option
        }
        
        if options['hanging_punctuation'] == 'none':
            options['hanging_punctuation'] = None

        # Создаем экземпляр типографа
        typo = Typographer(**options)
        
        # Обрабатываем текст
        processed = typo.process(text)
        
        return render(
            request, 
            template_name='typograph/result_fragment.html', 
            context={'processed_text': processed}
        )
    
    return HttpResponse(status=405)
