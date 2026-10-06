from pathlib import Path
from django.test import TestCase, Client, override_settings
from django.urls import reverse
from django.conf import settings


@override_settings(SECURE_SSL_REDIRECT=False)
class VendorAssetsAndFallbackTestCase(TestCase):
    """
    Тестирование наличия вендорных ассетов и корректности подключения fallback в шаблоне base.html.
    """

    def setUp(self):
        self.client = Client()

    def test_vendor_static_files_exist(self):
        """Проверяем, что все скомпилированные/скопированные локальные файлы присутствуют в статике."""
        static_dir = settings.BASE_DIR.parent / 'public' / 'static'
        
        required_files = [
            'vendor/bootstrap/bootstrap.min.css',
            'vendor/bootstrap/bootstrap.bundle.min.js',
            'vendor/bootstrap-icons/bootstrap-icons.min.css',
            'vendor/bootstrap-icons/fonts/bootstrap-icons.woff2',
            'vendor/bootstrap-icons/fonts/bootstrap-icons.woff',
            'vendor/htmx/htmx.min.js',
            'vendor/alpinejs/cdn.min.js',
            'codemirror/editor.js',
        ]

        for rel_path in required_files:
            file_path = static_dir / rel_path
            self.assertTrue(
                file_path.exists(),
                f"Файл вендора не найден в статике: {rel_path} (ожидался по пути {file_path})"
            )
            self.assertGreater(
                file_path.stat().st_size,
                0,
                f"Файл вендора пуст: {rel_path}"
            )

    def test_base_template_fallback_tags(self):
        """Проверяем, что главная страница отдает теги с fallback-обработкой ошибок загрузки с CDN."""
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)

        content = response.content.decode('utf-8')

        # Проверка fallback для Bootstrap CSS
        self.assertIn('bootstrap.min.css', content)
        self.assertIn("vendor/bootstrap/bootstrap.min.css", content)

        # Проверка fallback для Bootstrap Icons
        self.assertIn('bootstrap-icons.min.css', content)
        self.assertIn("vendor/bootstrap-icons/bootstrap-icons.min.css", content)

        # Проверка fallback для HTMX
        self.assertIn('htmx.org', content)
        self.assertIn('window.htmx || document.write', content)
        self.assertIn('vendor/htmx/htmx.min.js', content)

        # Проверка fallback для Alpine.js
        self.assertIn('alpinejs', content)
        self.assertIn('vendor/alpinejs/cdn.min.js', content)

        # Проверка fallback для Bootstrap JS
        self.assertIn('bootstrap.bundle.min.js', content)
        self.assertIn('window.bootstrap || document.write', content)
        self.assertIn('vendor/bootstrap/bootstrap.bundle.min.js', content)


@override_settings(SECURE_SSL_REDIRECT=False)
class TypographViewsTestCase(TestCase):
    """
    Базовые тесты функциональности представлений типографа.
    """

    def setUp(self):
        self.client = Client()

    def test_process_text_endpoint(self):
        """Проверка эндпоинта типографирования текста."""
        response = self.client.post(
            reverse('process_text'),
            data={
                'text': 'Тест "кавычек" и предлога в тексте.',
                'langs': 'ru',
                'quotes': 'on',
                'unbreakables': 'on',
            }
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn('X-Processing-Time', response.headers)
        content = response.content.decode('utf-8')
        # Проверяем типографирование кавычек «ёлочки»
        self.assertIn('«кавычек»', content)

    def test_stats_summary_endpoint(self):
        """Проверка эндпоинта сводной статистики."""
        response = self.client.get(reverse('stats_summary'))
        self.assertEqual(response.status_code, 200)

    def test_seo_metadata_and_sitemap(self):
        """Проверка мета-тегов на главной странице и генерации sitemap.xml."""
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        content = response.content.decode('utf-8')
        self.assertIn('<title>Онлайн-типограф', content)
        self.assertIn('name="description"', content)
        self.assertIn('name="keywords"', content)
        self.assertIn('rel="canonical"', content)

        # Проверка sitemap.xml
        sitemap_res = self.client.get('/sitemap.xml')
        self.assertEqual(sitemap_res.status_code, 200)
        sitemap_content = sitemap_res.content.decode('utf-8')
        self.assertIn('<loc>', sitemap_content)
        self.assertIn('http://testserver/', sitemap_content)
