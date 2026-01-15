FROM python:3.13-slim

# Настройки Python
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

# Установка Poetry
RUN pip install --no-cache-dir poetry

# Копируем файлы зависимостей
COPY pyproject.toml poetry.lock* /app/

# Настройка Poetry: не создавать venv и установка зависимостей (без dev-зависимостей для продакшена)
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --no-root --only main

# Создаем непривилегированного пользователя
RUN useradd -m -r appuser

# Копируем код проекта
COPY . /app/

# Меняем владельца папки
RUN chown -R appuser:appuser /app

# Переключаемся на пользователя
USER appuser

# Порт
EXPOSE 8000

# Команда запуска через Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "etpgrf_site.wsgi"]
