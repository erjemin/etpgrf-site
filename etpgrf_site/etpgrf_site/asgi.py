"""
ASGI config for etpgrf_site project.
"""

import os
from pathlib import Path
from django.core.asgi import get_asgi_application

# Пытаемся загрузить переменные из .env файла
try:
    from dotenv import load_dotenv
    env_path = Path(__file__).resolve().parent.parent.parent / '.env'
    load_dotenv(env_path)
except ImportError:
    pass

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'etpgrf_site.settings')

application = get_asgi_application()
