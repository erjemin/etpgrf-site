# Фронтенд: Структура и сборка

## 1. Стек и библиотеки
- **HTML / Django Templates:** шаблоны `base.html`, компоненты `typograph/` и `blog/`.
- **CSS:** Bootstrap 5, Bootstrap Icons, кастомные стили `public/static/css/etpgrf.css` с поддержкой темной/светлой темы.
- **Интерактивность:**
  - **HTMX:** асинхронные запросы (отправка формы типографирования, динамическое обновление плашки со статистикой без перезагрузки).
  - **Alpine.js:** управление состоянием клиентских виджетов и раскрывающихся списков опций.
- **Редактор текста:** CodeMirror 6.

## 2. Сборка фронтенда и вендорных библиотек (`frontend-assembly/`)
- Каталог `frontend-assembly/` управляет сборкой редактора и подготовкой локальных копий всех сторонних библиотек для автономной работы и CDN-fallback:
  - `src/editor.js`: инициализация CodeMirror 6, подсветка спецсимволов (`&nbsp;`, `&shy;`, тире, кавычки), интеграция темной/светлой темы.
  - `copy-vendor.js`: копирование дистрибутивов Bootstrap 5, Bootstrap Icons (включая шрифты), HTMX и Alpine.js из `node_modules` в `public/static/vendor/`.
  - `package.json`: зависимости `@codemirror/*`, `bootstrap`, `bootstrap-icons`, `htmx.org`, `alpinejs`, `esbuild`.
- Команды сборки:
  - `npm run build`: выполняет `build:codemirror` (сборка `editor.js`) и `build:vendor` (копирование всех библиотек в `static/vendor/`).
  - `npm run build:codemirror`: компилирует бандл в `public/static/codemirror/editor.js`.
  - `npm run build:vendor`: экспортирует вендорные CSS/JS/шрифты в `public/static/vendor/`.
  - `npm run watch`: отслеживание изменений CodeMirror в реальном времени.

## 3. CDN Fallback стратегия (`base.html`)
- Основные библиотеки подключаются из публичных CDN (jsDelivr, unpkg) для быстрой доставки и кэширования в браузерах.
- При блокировке или недоступности CDN срабатывает автоматический fallback на локальные статические копии:
  - **CSS (Bootstrap, Bootstrap Icons):** атрибут `onerror="this.onerror=null;this.href='{% static ... %}';"` на тегах `<link>`.
  - **JS (HTMX, Bootstrap Bundle):** проверка глобального объекта (`window.htmx`, `window.bootstrap`) и подгрузка локальной копии через `document.write`.
  - **JS (Alpine.js):** `onerror` динамически подключает локальный deferred-скрипт, а также предусмотрена резервная проверка в `DOMContentLoaded`.

## 4. Клиентская статика (`public/static/`)
- `css/etpgrf.css` — основные стили сайта, оформление типографа и блога.
- `js/base.js` — вспомогательные клиентские скрипты (обработка куки-баннера, копирование текста, переключение тем).
- `codemirror/` — собранный esm-бандл редактора.
- `vendor/` — локальные копии сторонних библиотек (`bootstrap`, `bootstrap-icons`, `htmx`, `alpinejs`).
- `svg/` и `img/` — векторные и растровые логотипы для светлой/темной темы и мета-тегов Open Graph.
