FROM python:3.13-slim

# Настройки Python
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

# Установка системных зависимостей (для сборки psycopg2 и работы poetry)
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && apt-get clean

# Установка Poetry
RUN pip install poetry

# Копируем файлы зависимостей
COPY pyproject.toml poetry.lock* /app/

# Настройка Poetry: не создавать venv (в докере он не нужен) и установка зависимостей
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --no-root

# Делаем зкркало всего кода проекта
COPY . /app/

# Порт, который будет слушать контейнер
EXPOSE 8000
