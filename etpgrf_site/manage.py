#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
from pathlib import Path


def main():
    """Run administrative tasks."""
    # Пытаемся загрузить переменные из .env файла
    try:
        from dotenv import load_dotenv
        # Ищем .env в корне проекта (на два уровня выше manage.py)
        # manage.py лежит в etpgrf_site/manage.py
        # .env лежит в 2026-etpgrf-site/.env
        env_path = Path(__file__).resolve().parent.parent / '.env'
        load_dotenv(env_path)
    except ImportError:
        pass  # Если python-dotenv не установлен, просто пропускаем

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'etpgrf_site.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
