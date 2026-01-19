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
  const TTL_MS = 90 * 24 * 60 * 60 * 1000; // 90 дней: 90 * 24 * 60 * 60 * 1000 = 7776000000)

  const banner = document.getElementById('cookie-banner');
  const acceptButton = document.getElementById('cookie-accept');

  // Функция загрузки счетчиков аналитики
  function loadCounters() {
    // console.log("Загрузка счетчиков (Яндекс, Google)...");
    // Код Яндекс.Метрики
    (function (m, e, t, r, i, k, a) {
      m[i] = m[i] || function () { (m[i].a = m[i].a || []).push(arguments) };
      m[i].l = 1 * new Date();
      for (var j = 0; j < document.scripts.length; j++) { if (document.scripts[j].src === r) { return; } }
      k = e.createElement(t), a = e.getElementsByTagName(t)[0], k.async = 1, k.src = r, a.parentNode.insertBefore(k, a)
    })(window, document, 'script', 'https://mc.yandex.ru/metrika/tag.js?id=106310834', 'ym');
    ym(106310834, 'init', {
      ssr: true, webvisor: true, clickmap: true, ecommerce: "dataLayer",
      accurateTrackBounce: true, trackLinks: true
    });

    // Код Google Analytics
    // window.dataLayer = window.dataLayer || [];
    // function gtag(){dataLayer.push(arguments);}
    // gtag('js', new Date());
    // gtag('config', 'G-XXXXXXXXXX');

    // Код Top.Mail.Ru
    var _tmr = window._tmr || (window._tmr = []);
    _tmr.push({id: "3734603", type: "pageView", start: (new Date()).getTime()});
    (function (d, w, id) {
      if (d.getElementById(id)) return;
      var ts = d.createElement("script");
      ts.type = "text/javascript"; ts.async = true; ts.id = id; ts.src = "https://top-fwz1.mail.ru/js/code.js";
      var f = function () {
        var s = d.getElementsByTagName("script")[0]; s.parentNode.insertBefore(ts, s);
      };
      if (w.opera == "[object Opera]") {
        d.addEventListener("DOMContentLoaded", f, false);
      } else { f(); }
    })(document, window, "tmr-code");
    // <noscript><div><img src="https://top-fwz1.mail.ru/counter?id=3734603;js=na" style="position:absolute;left:-9999px;" alt="Top.Mail.Ru" /></div></noscript>
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