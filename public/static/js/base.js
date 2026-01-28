(function () {
    "use strict";

    // --- АВТОМАТИЧЕСКОЕ ПЕРЕКЛЮЧЕНИЕ ТЕМЫ (Dark/Light) ---
    const darkModeMediaQuery = window.matchMedia('(prefers-color-scheme: dark)');

    function updateTheme(e) {
        const theme = e.matches ? 'dark' : 'light';
        document.documentElement.setAttribute('data-bs-theme', theme);
    }

    // Установить при загрузке
    updateTheme(darkModeMediaQuery);
    // Слушать изменения
    darkModeMediaQuery.addEventListener('change', updateTheme);

    // --- ЛОГОТИП И СКРОЛЛ ---
    function updateLogo() {
        const navbar = document.getElementById('logo');
        if (!navbar) return;
        
        const scrollY = window.scrollY;

        // Гистерезис: включаем после 60px, выключаем до 10px
        // Это предотвращает дребезг на границе
        if (scrollY > 60) {
            navbar.classList.remove('logo-big');
        } else if (scrollY < 10) {
            navbar.classList.add('logo-big');
        }
    }

    // Инициализация логотипа при загрузке и скролле
    window.addEventListener('scroll', updateLogo, { passive: true });
    
    // --- МОБИЛЬНОЕ МЕНЮ (Скрытие логотипа при открытии) ---
    document.addEventListener('DOMContentLoaded', function() {
        const navbarNav = document.getElementById('navbarNav');
        const navbarBrand = document.querySelector('.navbar-brand');
        
        if (navbarNav && navbarBrand) {
            navbarNav.addEventListener('show.bs.collapse', function () {
                navbarBrand.style.opacity = '0';
                navbarBrand.style.transition = 'opacity 0.3s ease';
            });
            
            navbarNav.addEventListener('hide.bs.collapse', function () {
                navbarBrand.style.opacity = '1';
            });
        }
    });

    // --- КУКИ И СЧЕТЧИКИ ---
    const COOKIE_KEY = 'cookie_consent';
    const TTL_MS = 90 * 24 * 60 * 60 * 1000; // 90 дней
    const MAILRU_ID = "3734603";
    const YANDEX_ID = "106310834";
    const GOOGLE_ID = "G-03WY2S9FXB";

    function loadCounters() {
        // console.log("Загрузка счетчиков...");
        try {
            // Mail.ru
            var _tmr = window._tmr || (window._tmr = []);
            _tmr.push({id: MAILRU_ID, type: "pageView", start: (new Date()).getTime()});
            (function (d, w, id) {
              if (d.getElementById(id)) return;
              var ts = d.createElement("script"); ts.type = "text/javascript"; ts.async = true; ts.id = id;
              ts.src = "https://top-fwz1.mail.ru/js/code.js";
              var f = d.getElementsByTagName("script")[0]; f.parentNode.insertBefore(ts, f);
            })(document, window, "topmailru-code");
            
            // Яндекс.Метрика
            (function(m,e,t,r,i,k,a){m[i]=m[i]||function(){(m[i].a=m[i].a||[]).push(arguments)};
            m[i].l=1*new Date();
            for (var j = 0; j < document.scripts.length; j++) {if (document.scripts[j].src === r) { return; }}
            k=e.createElement(t),a=e.getElementsByTagName(t)[0],k.async=1,k.src=r,a.parentNode.insertBefore(k,a)})
            (window, document, "script", "https://mc.yandex.ru/metrika/tag.js", "ym");

            window.ym(YANDEX_ID, "init", {
                 clickmap:true,
                 trackLinks:true,
                 accurateTrackBounce:true
            });
            
            // Google Analytics
            (function() {
                var script = document.createElement('script');
                script.async = true;
                script.src = 'https://www.googletagmanager.com/gtag/js?id=' + GOOGLE_ID;
                document.head.appendChild(script);
            })();

            window.dataLayer = window.dataLayer || [];
            function gtag(){dataLayer.push(arguments);}
            // Делаем gtag глобальной, чтобы вызывать из sendGoal
            window.gtag = gtag; 
            gtag('js', new Date());
            gtag('config', '\'' + GOOGLE_ID + '\'');
            
        } catch (e) {
            console.error("Ошибка загрузки счетчиков:", e);
        }
    }

    function checkConsent() {
        try {
            const stored = localStorage.getItem(COOKIE_KEY);
            if (!stored) return false;
            const data = JSON.parse(stored);
            const now = Date.now();
            if (now - data.timestamp > TTL_MS) {
                localStorage.removeItem(COOKIE_KEY);
                return false;
            }
            return true;
        } catch (e) {
            return false;
        }
    }

    // Инициализация куки-баннера
    document.addEventListener('DOMContentLoaded', function() {
        const banner = document.getElementById('cookie-banner');
        const acceptButton = document.getElementById('cookie-accept');

        if (banner && acceptButton) {
            if (checkConsent()) {
                loadCounters();
            } else {
                banner.style.display = 'block';
            }

            acceptButton.addEventListener('click', function () {
                const data = { value: true, timestamp: Date.now() };
                localStorage.setItem(COOKIE_KEY, JSON.stringify(data));
                banner.style.display = 'none';
                loadCounters();
            });
        }
    });
    
    // Глобальная функция для отправки целей
    window.sendGoal = function(goalName) {
        if (!checkConsent()) return;
        // console.log("Sending goal:", goalName);
        
        try {
            // Mail.ru
            if (window._tmr) {
                window._tmr.push({ id: MAILRU_ID, type: "reachGoal", goal: goalName, value: 1 });
            }
            // Яндекс.Метрика
            if (typeof window.ym === 'function') {
                window.ym(YANDEX_ID, 'reachGoal', goalName);
            }
            // Google Analytics
            if (typeof window.gtag === 'function') {
                window.gtag('event', goalName);
            }
        } catch (e) {
            console.error("Ошибка отправки цели:", e);
        }
    };
})();
