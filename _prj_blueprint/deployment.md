# Деплой, окружение и регламент релизов

## 1. Конфигурация окружения (.env)
Обязательные переменные:
- `SECRET_KEY`: секретный ключ Django.
- `DEBUG`: `True` для локальной разработки, `False` для продакшена.
- `ALLOWED_HOSTS`: разрешенные хосты через запятую (например, `typograph.cube2.ru,localhost`).
- `CSRF_TRUSTED_ORIGINS`: доверенные URL (например, `https://typograph.cube2.ru,http://localhost:8000`).
- `ADMIN_URL`: путь к панели администратора (например, `mysecretadmin/`).

## 2. Docker и инфраструктура
- **`Dockerfile`**: базовый образ `python:3.13-slim`, установка Poetry, сборка зависимостей, запуск через Gunicorn.
- **`docker-compose.yml`**: конфигурация для разработки (монтирование исходного кода, базы данных и папок статики/медиа).
- **`docker-compose.prod.yml`**: конфигурация для продакшена со связанным сервисом Nginx (`config/nginx/`).

## 3. Чек-лист выпуска релиза (согласно NOTE.md)
Перед созданием релизного тега:
1. Протестировать функционал и миграции.
2. Внести описание изменений в `CHANGELOG.md`.
3. Обновить версии в:
   - `pyproject.toml` (командой `poetry version patch` или вручную).
   - `etpgrf_site/__init__.py` (при наличии `__version__`).
   - `etpgrf_site/typograph/templates/typograph/base.html` (версия библиотеки и версия сайта в футере).
4. Закоммитить изменения:
   ```bash
   git add .
   git commit -am "Обновление версии для релиза vX.Y.Z"
   git push origin main
   ```
5. Запустить пайплайн сборки и деплоя через Gitea Actions путем простановки тега:
   ```bash
   git tag vX.Y.Z && git push origin vX.Y.Z
   ```
