"""
WSGI config for etpgrf_site project.
"""

import os
from pathlib import Path
from django.core.wsgi import get_wsgi_application

# Пытаемся загрузить переменные из .env файла
try:
    from dotenv import load_dotenv
    # wsgi.py лежит в etpgrf_site/etpgrf_site/wsgi.py
    # .env лежит в 2026-etpgrf-site/.env (на три уровня выше)
    env_path = Path(__file__).resolve().parent.parent.parent / '.env'
    load_dotenv(env_path)
except ImportError:
    pass

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'etpgrf_site.settings')

application = get_wsgi_application()
