# --- Stage 1: Сборка фронтенда (CodeMirror) ---
FROM node:20-slim as frontend-builder

WORKDIR /app/frontend

# Копируем файлы зависимостей
COPY frontend-assembly/package.json frontend-assembly/package-lock.json ./

# Устанавливаем зависимости (включая devDependencies для сборки)
RUN npm ci

# Копируем исходники
COPY frontend-assembly/ ./

# Собираем бандл через npm script
RUN npm run build


# --- Stage 2: Сборка бэкенда (Django) ---
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

# Создаем папку для данных и статики, чтобы у appuser были права
RUN mkdir -p /app/data /app/public/static_collected

# Копируем собранный фронтенд из первого стейджа
COPY --from=frontend-builder /app/frontend/dist/editor.js /app/public/static/codemirror/editor.js

# Меняем владельца папки
RUN chown -R appuser:appuser /app

# Переключаемся на пользователя
USER appuser

# Порт
EXPOSE 8000

# Команда запуска через Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--chdir", "/app/etpgrf_site", "etpgrf_site.wsgi"]
