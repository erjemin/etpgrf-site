# Архитектурный обзор проекта ETPGRF Site

## 1. Назначение проекта
**ETPGRF Site** — веб-сервис и интерфейс для онлайн-типографирования текстов на базе библиотеки `etpgrf`, а также контентная платформа (блог, справочные и статические страницы, статистика использования).

## 2. Технологический стек
- **Backend:** Python 3.13+, Django 6.0+, Poetry.
- **База данных:** SQLite 3 (файл `data/db-etpgrf.sqlite3` с увеличенным таймаутом блокировки).
- **Frontend:**
  - Bootstrap 5 (CSS, сетка, компоненты, иконки bootstrap-icons).
  - Alpine.js (декларативное состояние на клиенте).
  - HTMX (динамическая подгрузка фрагментов, отправка форм типографирования, статистика).
  - CodeMirror 6 (продвинутый редактор текста с подсветкой спецсимволов/сущностей).
  - Сборщик фронтенда: `esbuild` в каталоге `frontend-assembly/`.
- **Инфраструктура & Деплой:**
  - Docker & Docker Compose (`docker-compose.yml` для разработки, `docker-compose.prod.yml` для продакшена).
  - Nginx (раздача статики `/static/` и медиа `/media/`, SSL-терминация, обратное проксирование к Gunicorn).
  - Gunicorn (WSGI-сервер Django).
  - CI/CD: Gitea Actions (автосборка Docker-образов по тегам `v*` и деплой).

## 3. Структура директорий
```
2026-etpgrf-site/
├── .github/                      # Инструкции для AI и CI
│   └── copilot-instructions.md
├── _prj_blueprint/               # Быстрый контекст и документация архитектуры
├── config/                       # Конфигурационные файлы Nginx
│   └── nginx/
├── data/                         # Хранилище базы данных SQLite (db-etpgrf.sqlite3)
├── etpgrf_site/                  # Исходный код Django
│   ├── manage.py
│   ├── etpgrf_site/              # Корневой модуль конфигурации (settings, urls, wsgi)
│   ├── typograph/                # Приложение типографа (обработка, DailyStat, UI)
│   └── blog/                     # Приложение блога и статических страниц
├── frontend-assembly/            # Node.js окружение сборки CodeMirror 6 (esbuild)
├── media/                        # Загружаемые медиа-файлы (обложки постов)
├── public/                       # Статика проекта
│   ├── static/                   # Исходная статика (css, js, img, svg, codemirror)
│   └── static_collected/         # Собранная статика collectstatic
├── Dockerfile                    # Сборка продакшн-образа
├── docker-compose.yml            # Dev-окружение
├── docker-compose.prod.yml       # Prod-окружение
├── pyproject.toml                # Poetry зависимости и метаданные
├── NOTE.md                       # Инструкции по релизам и версионированию
└── CHANGELOG.md                  # История версий
```

## 4. Ссылки на детальные описания
- [Бэкенд и логика приложений](backend.md)
- [Фронтенд и сборка](frontend.md)
- [Деплой, окружение и релизный процесс](deployment.md)
