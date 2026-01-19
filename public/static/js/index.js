// Импортируем из локального бандла (относительный путь)
import {
  EditorView,
  EditorState,
  lineNumbers,
  highlightActiveLineGutter,
  highlightWhitespace,
  highlightTrailingWhitespace,
  drawSelection,
  keymap,
  highlightSpecialChars,
  html,
  oneDark,
  syntaxHighlighting,
  defaultHighlightStyle,
  bracketMatching,
  defaultKeymap,
  Compartment
} from "../codemirror/editor.js";

const resultWrapper = document.getElementById('cm-result-wrapper');
const btnCopy = document.getElementById('btn-copy');
const sourceTextarea = document.querySelector('textarea[name="text"]');

// console.log("Index.js loaded. btnCopy:", !!btnCopy, "sourceTextarea:", !!sourceTextarea); // DEBUG

const themeCompartment = new Compartment();
function getTheme() {
  return window.matchMedia('(prefers-color-scheme: dark)').matches ? oneDark : [];
}

// Словарь названий для спецсимволов
const charNames = {
  0x00A0: "NoBreakable Space (неразрывный пробел — &nbsp;)",
  0x00AD: "Soft Hyphen (мягкий перенос — &shy;)",
  0x2002: "En Space (полужирный пробел — &ensp;)",
  0x2003: "Em Space (жирный пробел — &emsp;)",
  0x2007: "Figure Space (цифровой пробел — &numsp;)",
  0x2008: "Punctuation Space (пунктуационный пробел — &puncsp;)",
  0x2009: "Thin Space (тонкий пробел — &thinsp;)",
  0x200A: "Hair Space (толщина волоса — &hairsp;)",
  0x200B: "Negative Space (негативный пробел — &NegativeThinSpace;)",
  0x200C: "Zero Width Non-Joiner (пробел нулевой ширины, без объединения — &zwj;)",
  0x200D: "Zero Width Joiner (пробел нулевой ширины, с объединением — &zwnj;)",
  0x200E: "Left-to-Right Mark (изменить направление текста на слева-направо — &lrm;)",
  0x200F: "Right-to-Left Mark (изменить направление текста на справа-налево — &rlm;)",
  0x205F: "Medium Mathematical Space (средний пробел — &MediumSpace;)",
  0x2060: "NoBreak (без разрыва — &NoBreak;)",
  0x2062: "Invisible Times (невидимое умножение для семантической разметки математических выражений — &InvisibleTimes;)",
  0x2063: "Invisible Comma (невидимая запятая для семантической разметки математических выражений — &InvisibleComma;)",
};

const PLACEHOLDER_TEXT = "Здесь появится результат...";

const resultState = EditorState.create({
  doc: PLACEHOLDER_TEXT,
  extensions: [
    lineNumbers(),
    highlightActiveLineGutter(),
    // Подсветка NBSP и других специальных пробелов
    highlightSpecialChars({
      specialChars: /[\u2002\u00AD\u2003\u2007\u2009\u00a0\u200A\u200B\u200C\u200D\u200E\u200F\u205F\u2060\u2062\u2063]/,
      addSpecialChars: true,
      render: (code) => {
        let span = document.createElement("span");
        span.textContent = "•";
        span.style.background = "#ff000044";  // Полупрозрачный красный фон
        span.style.color = "#ffff00";  // Желтый цвет точки
        // Используем словарь для title
        span.title = "U+" + code.toString(16).toUpperCase().padStart(4, '0') + " / " + (charNames[code] || "Special Char");
        return span;
      }
    }),
    highlightWhitespace(),
    highlightTrailingWhitespace(),
    drawSelection(),
    syntaxHighlighting(defaultHighlightStyle, {fallback: true}),
    bracketMatching(),
    keymap.of(defaultKeymap),
    html(),
    themeCompartment.of(getTheme()),
    EditorState.readOnly.of(true)
  ]
});

const resultView = new EditorView({
  state: resultState,
  parent: resultWrapper
});

// Обработка ответа от сервера (HTMX)
document.body.addEventListener('htmx:afterSwap', function (evt) {
  // console.log("HTMX afterSwap event:", evt.detail.target.id); // DEBUG
  if (evt.detail.target.id === 'result-area') {
    const newContent = evt.detail.xhr.response;
    
    // Обновляем редактор
    resultView.dispatch({
      changes: {from: 0, to: resultView.state.doc.length, insert: newContent}
    });
    
    // Показываем кнопку копирования
    if (btnCopy) {
        // console.log("Showing copy button"); // DEBUG
        btnCopy.classList.remove('d-none');
    }
  }
});

// Скрываем кнопку и сбрасываем редактор при изменении исходного текста
if (sourceTextarea) {
  sourceTextarea.addEventListener('input', () => {
    if (btnCopy) {
      btnCopy.classList.add('d-none');
    }
    // Сбрасываем редактор на плейсхолдер
    if (resultView.state.doc.toString() !== PLACEHOLDER_TEXT) {
        resultView.dispatch({
          changes: {from: 0, to: resultView.state.doc.length, insert: PLACEHOLDER_TEXT}
        });
    }
  });
}

window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', () => {
  resultView.dispatch({
    effects: themeCompartment.reconfigure(getTheme())
  });
});

// --- КОПИРОВАНИЕ В БУФЕР ---
if (btnCopy) {
  btnCopy.addEventListener('click', async () => {
    const text = resultView.state.doc.toString();
    // console.log("Copying text:", text.substring(0, 20) + "..."); // DEBUG
    
    // Отправляем цель в метрику
    if (typeof window.sendGoal === 'function') {
        window.sendGoal('etpgrf-copy-pressed');
    }
    
    try {
      await navigator.clipboard.writeText(text);
      
      // Визуальное подтверждение
      const originalHtml = btnCopy.innerHTML;
      const originalClass = btnCopy.className; 
      
      btnCopy.innerHTML = '<i class="bi bi-check-lg me-1"></i> Скопировано!';
      btnCopy.classList.remove('btn-outline-secondary', 'btn-outline-primary');
      btnCopy.classList.add('btn-success');
      
      setTimeout(() => {
        btnCopy.innerHTML = originalHtml;
        btnCopy.className = originalClass;
        btnCopy.classList.remove('d-none'); 
      }, 2000);
      
    } catch (err) {
      console.error('Ошибка копирования:', err);
      alert('Не удалось скопировать текст.');
    }
  });
}
