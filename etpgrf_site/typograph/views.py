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
        layout_enabled = request.POST.get(key='layout') == 'on'
        layout_option = False
        if layout_enabled:
            process_units = request.POST.get(key='layout_units') == 'on'
            if process_units:
                custom_units = request.POST.get(key='layout_units_custom', default='').strip()
                if custom_units:
                    process_units = custom_units.split()
            
            layout_option = LayoutProcessor(
                langs=langs,
                process_initials_and_acronyms=request.POST.get(key='layout_initials') == 'on',
                process_units=process_units
            )
            
        # 3. Собираем Hyphenator
        hyphenation_enabled = request.POST.get(key='hyphenation') == 'on'
        hyphenation_option = False
        if hyphenation_enabled:
            max_len = request.POST.get(key='hyphenation_len', default='12')
            try:
                max_len = int(max_len)
            except (ValueError, TypeError):
                max_len = 12
            
            hyphenation_option = Hyphenator(
                langs=langs,
                max_unhyphenated_len=max_len
            )

        # 4. Читаем Sanitizer
        sanitizer_enabled = request.POST.get(key='sanitizer_enabled') == 'on'
        sanitizer_option = None
        if sanitizer_enabled:
            sanitizer_option = request.POST.get(key='sanitizer', default='etp')

        # 5. Читаем Hanging Punctuation
        hanging_enabled = request.POST.get(key='hanging_enabled') == 'on'
        hanging_option = None
        if hanging_enabled:
            hanging_option = request.POST.get(key='hanging_punctuation', default='both')

        # 6. Собираем общие опции
        options = {
            'langs': langs,
            'process_html': True,
            'quotes': request.POST.get('quotes') == 'on',
            'layout': layout_option,
            'unbreakables': request.POST.get(key='unbreakables') == 'on',
            'hyphenation': hyphenation_option,
            'symbols': request.POST.get(key='symbols') == 'on',
            'hanging_punctuation': hanging_option,
            'mode': request.POST.get(key='mode', default='mixed'),
            'sanitizer': sanitizer_option
        }
        
        # --- ДИАГНОСТИКА ---
        # print("Typographer options:", options)
        # -------------------

        # Создаем экземпляр типографа
        typo = Typographer(**options)
        
        # Обрабатываем текст
        processed = typo.process(text)
        print("Processed text length:", len(processed))
        print("Processed text:", processed)
        
        return render(
            request, 
            template_name='typograph/result_fragment.html', 
            context={'processed_text': processed}
        )
    
    return HttpResponse(status=405)
