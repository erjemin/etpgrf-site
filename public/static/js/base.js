(function () {
  const darkModeMediaQuery = window.matchMedia('(prefers-color-scheme: dark)');
  const logoImg = document.getElementById('logo-img');
  const navbar = document.getElementById('main-navbar');

  // --- АВТОМАТИЧЕСКОЕ ПЕРЕКЛЮЧЕНИЕ ТЕМЫ (Dark/Light) ---
  function updateTheme(e) {
    const theme = e.matches ? 'dark' : 'light';
    document.documentElement.setAttribute('data-bs-theme', theme);
  }

  // --- ОБНОВЛЕНИЕ ЛОГОТИПА ПРИ СКРОЛЛЕ И СМЕНЕ ТЕМЫ ---
  function updateLogo() {
    const isDark = darkModeMediaQuery.matches;
    // Используем getBoundingClientRect для определения позиции контента
    if (document.getElementById('content-container').getBoundingClientRect().top < 78) {
      navbar.classList.add('navbar-scrolled');
      logoImg.src = isDark ? logoImg.dataset.srcDarkCompact : logoImg.dataset.srcLightCompact;
    } else {
      navbar.classList.remove('navbar-scrolled');
      logoImg.src = isDark ? logoImg.dataset.srcDark : logoImg.dataset.srcLight;
    }
  }

  // Инициализация
  updateTheme(darkModeMediaQuery);
  updateLogo();
  document.addEventListener('DOMContentLoaded', updateLogo);

  // Слушаем скролл
  window.addEventListener('scroll', updateLogo);

  // Слушаем смену темы
  window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', updateLogo);

  // --- КУКИ ---
  const COOKIE_KEY = 'cookie_consent';
  const TTL_MS = 60 * 1000; // 1 минута для отладки (потом поставить 90 дней: 90 * 24 * 60 * 60 * 1000 = 7776000000)

  const banner = document.getElementById('cookie-banner');
  const acceptButton = document.getElementById('cookie-accept');

  function loadCounters() {
    console.log("Загрузка счетчиков (Яндекс, Google)...");
    // Код Яндекс.Метрики
    // (function(m,e,t,r,i,k,a){...})(window, document, "script", "https://mc.yandex.ru/metrika/tag.js", "ym");
    // ym(XXXXXX, "init", {...});

    // Код Google Analytics
    // window.dataLayer = window.dataLayer || [];
    // function gtag(){dataLayer.push(arguments);}
    // gtag('js', new Date());
    // gtag('config', 'G-XXXXXXXXXX');

    // Код Top.Mail.Ru
    // (function(w, d, c) { ... })(window, document, "topmailru");

    // и т.д.

    // alert("Отладка. Счетчики загружены (здесь должен быть реальный код счетчиков).");
  }

  function checkConsent() {
    const stored = localStorage.getItem(COOKIE_KEY);
    if (!stored) return false;

    try {
      const data = JSON.parse(stored);
      const now = Date.now();
      // Проверяем, не истек ли срок
      if (now - data.timestamp > TTL_MS) {
        localStorage.removeItem(COOKIE_KEY);
        return false;
      }
      return true;
    } catch (e) {
      return false;
    }
  }

  if (checkConsent()) {
    loadCounters();
  } else {
    banner.style.display = 'block';
  }

  acceptButton.addEventListener('click', function () {
    const data = {
      value: true,
      timestamp: Date.now()
    };
    localStorage.setItem(COOKIE_KEY, JSON.stringify(data));
    banner.style.display = 'none';
    loadCounters();
  });
})();