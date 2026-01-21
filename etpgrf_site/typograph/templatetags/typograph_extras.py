from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter(name='humanize_num')
def humanize_num(value):
    """
    Форматирует число с тонкими пробелами в качестве разделителя тысяч
    и сокращает большие числа до M (миллионы) или k (тысячи).
    
    Примеры:
    1234 -> 1&thinsp;234
    1234567 -> 1,2M
    """
    try:
        num = int(value)
        if num > 1_000_000_000:
            val = num / 1_000_000_000
            suffix = "&thinsp;B"
        elif num > 1_000_000:
            val = num / 1_000_000
            suffix = "&thinsp;M"
        elif num > 1_000:
            val = num / 1_000
            suffix = "&thinsp;k"
        else:
            # Больше 1B -- форматируем с пробелами
            return mark_safe(f"{num:,}".replace(",", "&thinsp;"))

        # Форматируем float:
        # {:,.1f} - разделитель тысяч (запятая) и 1 знак после точки
        # 1234567.89 -> "1,234,567.9"
        formatted = f"{val:,.2f}"
        
        # Меняем английскую запятую (разделитель тысяч) на тонкий пробел
        # Меняем английскую точку (десятичный разделитель) на запятую
        # Но тут проблема: replace делает все сразу.
        # "1,234.5" -> replace(",", " ") -> "1 234.5" -> replace(".", ",") -> "1 234,5"
        formatted = formatted.replace(",", "&thinsp;").replace(".", ",")
        
        return mark_safe(f"{formatted}{suffix}")

    except (ValueError, TypeError):
        return value
