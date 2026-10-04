# Бэкенд: Архитектура и модули

## 1. Django Конфигурация (`etpgrf_site/etpgrf_site/`)
- **`settings.py`**:
  - `DEBUG` и `SECRET_KEY` считываются из переменных окружения.
  - `ADMIN_URL`: настраиваемый префикс панели администратора (по умолчанию `admin/`).
  - База данных: SQLite в `data/db-etpgrf.sqlite3` с `timeout: 20` для надежности при конкурентных запросах.
  - Статика: `STATICFILES_DIRS = [BASE_DIR.parent / 'public' / 'static']`, `STATIC_ROOT = BASE_DIR.parent / 'public' / 'static_collected'`.
  - Медиа: `MEDIA_ROOT = BASE_DIR.parent / 'media'`, `MEDIA_URL = '/media/'`.
  - Защита за прокси: в `not DEBUG` активированы `SECURE_PROXY_SSL_HEADER`, `SECURE_SSL_REDIRECT`, `SESSION_COOKIE_SECURE`, `CSRF_COOKIE_SECURE`, `USE_X_FORWARDED_HOST`, `USE_X_FORWARDED_PORT`.
- **`urls.py`**:
  - `/{ADMIN_URL}` -> админка Django.
  - `/` -> `typograph.urls` (главная страница типографа, API обработки и статистики).
  - `/blog/` -> `blog.urls` (список постов, детальная страница поста).
  - `/sitemap.xml` -> карта сайта (`PostSitemap`).
  - `/<slug:slug>/` -> ловушка для статических страниц (например, `/about/`, `/privacy-policy/`, `/donate/`).

## 2. Приложение `typograph`
Отвечает за взаимодействие с библиотекой типографирования `etpgrf` и сбор агрегированной аналитики.

### Модели (`typograph/models.py`)
- **`DailyStat`**:
  - Агрегированные посуточные показатели (`date` - уникальная дата).
  - Метрики активности: `index_views`, `process_requests`, `copy_count`.
  - Объемы данных: `chars_in`, `chars_out`, `chars_copied`.
  - Производительность: `total_processing_time_ms`, вычисляемое свойство `avg_processing_time_ms`.
  - `settings_stats`: JSONField со статистикой популярности опций (языки, кавычки, переносы, висячая пунктуация и т.д.).

### Представления и Эндпоинты (`typograph/views.py`)
- `index` (`/`): главная страница, инкрементирует просмотры `index_views`.
- `process_text` (`/process/`, POST):
  - Принимает текст и параметры типографирования из формы.
  - Инициализирует `LayoutProcessor`, `Hyphenator`, `Typographer` из пакета `etpgrf`.
  - Производит замер времени обработки `time.perf_counter()`.
  - Атомарно обновляет счетчики в `DailyStat`.
  - Возвращает HTML-фрагмент `typograph/result_fragment.html` и заголовок `X-Processing-Time`.
- `track_copy` (`/track-copy/`, POST): фиксирует факт и длину скопированного в буфер текста.
- `get_stats_summary` (`/stats-summary/`, GET): возвращает компактный HTMX-фрагмент со статистикой для футера.

## 3. Приложение `blog`
Отвечает за публикации, статьи и произвольные статические страницы.

### Модели (`blog/models.py`)
- **`Post`**:
  - `post_type`: `B` (Пост блога) или `P` (Страница).
  - `title`, `slug` (автоматическая транслитерация через `pytils.translit.slugify` с обработкой коллизий).
  - `is_published`, `published_at`, `updated_at`.
  - `content` (HTML-разметка), `excerpt` (тизер).
  - `image` (обложка для превью и Open Graph).
  - SEO-поля: `seo_title`, `seo_description`, `seo_keywords`.
  - Метод `get_absolute_url()`: возвращает `/blog/<slug>/` для постов или `/<slug>/` для страниц.

### Представления (`blog/views.py`)
- `post_list` (`/blog/`): список опубликованных статей блога с пагинацией.
- `post_detail` (`/blog/<slug>/`): детальная страница поста с Open Graph мета-тегами и разметкой.
- `page_detail` (`/<slug>/`): отображение статических страниц.
- `sitemaps.py`: генерация `sitemap.xml` по опубликованным записям.
