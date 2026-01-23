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
        if (!navbar) return;
        const navbar = document.getElementById('logo');
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

    // --- КУКИ И СЧЕТЧИКИ ---
    const COOKIE_KEY = 'cookie_consent';
    const TTL_MS = 90 * 24 * 60 * 60 * 1000; // 90 дней
    const MAILRU_ID = "3734603";
    const YANDEX_ID = "106310834";

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
            if (window._tmr) {
                window._tmr.push({ id: MAILRU_ID, type: "reachGoal", goal: goalName, value: 1 });
            }
            if (typeof window.ym === 'function') {
                window.ym(YANDEX_ID, 'reachGoal', goalName);
            }
        } catch (e) {
            console.error("Ошибка отправки цели:", e);
        }
    };
})();
