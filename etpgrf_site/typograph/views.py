from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.db.models import F, Sum
from django.utils import timezone
from django.views.decorators.http import require_POST
from etpgrf.typograph import Typographer
from etpgrf.layout import LayoutProcessor
from etpgrf.hyphenation import Hyphenator
from .models import DailyStat
import time


def index(request):
    # Увеличиваем счетчик просмотров главной
    try:
        today = timezone.now().date()
        stat, created = DailyStat.objects.get_or_create(date=today)
        DailyStat.objects.filter(pk=stat.pk).update(index_views=F('index_views') + 1)
    except Exception as e:
        print(f"Stat error: {e}")

    return render(request, template_name='typograph/index.html')


def get_stats_summary(request):
    """Возвращает сводную статистику."""
    try:
        stats = DailyStat.objects.aggregate(
            views=Sum('index_views'),
            processed=Sum('process_requests'),
            copied=Sum('copy_count'),
            chars_in=Sum('chars_in'),
            chars_out=Sum('chars_out'),
            chars_copied=Sum('chars_copied')
        )
        
        context = {
            'views': stats['views'] or 0,
            'processed': stats['processed'] or 0,
            'copied': stats['copied'] or 0,
            'chars_in': stats['chars_in'] or 0,
            'chars_out': stats['chars_out'] or 0,
            'chars_copied': stats['chars_copied'] or 0,
        }

        return render(request, 'typograph/stats_summary.html', context)
    except Exception:
        return HttpResponse("...")


@require_POST
def track_copy(request):
    """Увеличивает счетчик копирований и количество скопированных символов."""
    try:
        char_count = int(request.POST.get('char_count', 0))
        
        today = timezone.now().date()
        stat, created = DailyStat.objects.get_or_create(date=today)
        DailyStat.objects.filter(pk=stat.pk).update(
            copy_count=F('copy_count') + 1,
            chars_copied=F('chars_copied') + char_count
        )
        return HttpResponse("OK")
    except (ValueError, TypeError):
        return HttpResponse("Invalid char_count", status=400)
    except Exception as e:
        print(f"Stat error: {e}")
        return HttpResponse("Error", status=500)


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
            'sanitizer': sanitizer_option,
        }

        # Обрабатываем текст с замером времени
        start_time = time.perf_counter()
        # Создаем экземпляр типографа и передаем настройки в него
        typo = Typographer(**options)
        # Обрабатываем текст в Типографе
        processed = typo.process(text)
        end_time = time.perf_counter()
        
        duration_ms = (end_time - start_time) * 1000
        
        # --- СБОР СТАТИСТИКИ ---
        try:
            today = timezone.now().date()
            stat, created = DailyStat.objects.get_or_create(date=today)
            
            # 1. Атомарное обновление счетчиков
            DailyStat.objects.filter(pk=stat.pk).update(
                process_requests=F('process_requests') + 1,
                chars_in=F('chars_in') + len(text),
                chars_out=F('chars_out') + len(processed),
                total_processing_time_ms=F('total_processing_time_ms') + duration_ms
            )
            
            # 2. Обновление JSON с настройками (не атомарно, а значит при высокой нагрузке возможны потери данных)
            # Перечитываем объект, чтобы получить актуальный JSON
            stat.refresh_from_db()
            current_stats = stat.settings_stats
            
            def inc_stat(key, value):
                k = f"{key}:{value}"
                current_stats[k] = current_stats.get(k, 0) + 1

            # Собираем статистику по опциям
            # langs может быть строкой или списком
            lang_val = options['langs']
            if isinstance(lang_val, list):
                lang_val = lang_val[0] if lang_val else 'ru'
            inc_stat('lang', lang_val)
            
            inc_stat('mode', options['mode'])
            
            if options['quotes']: inc_stat('feature', 'quotes')
            if layout_enabled: inc_stat('feature', 'layout')
            if options['unbreakables']: inc_stat('feature', 'unbreakables')
            if hyphenation_enabled: inc_stat('feature', 'hyphenation')
            if options['symbols']: inc_stat('feature', 'symbols')
            if hanging_enabled: inc_stat('feature', 'hanging')
            if sanitizer_enabled: inc_stat('feature', 'sanitizer')
            
            stat.settings_stats = current_stats
            stat.save(update_fields=['settings_stats'])
            
        except Exception as e:
            print(f"Stat error: {e}")
        # -----------------------

        response = render(
            request,
            template_name='typograph/result_fragment.html',
            context={'processed_text': processed}
        )
        
        # Добавляем заголовок с временем обработки (с запятой вместо точки)
        response['X-Processing-Time'] = f"{duration_ms:.4f}".replace('.', ',')
        
        return response

    return HttpResponse(status=405)
