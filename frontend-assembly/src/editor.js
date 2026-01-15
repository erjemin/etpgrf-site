// =============================================================================
// Сборка CodeMirror 6 для проекта ETPGRF
// =============================================================================
// Этот файл служит точкой входа для esbuild.
// Мы экспортируем только те модули, которые реально используются в index.html.
// esbuild автоматически выбросит весь неиспользуемый код (Tree Shaking -- перетряхивание дерева).

// --- ЯДРО (State) ---
export {
  EditorState,              // Хранит состояние редактора (текст, выделение, конфигурацию).
  Compartment,              // Позволяет динамически менять части конфигурации (например, тему).
} from "@codemirror/state";

// --- ВИД (View) ---
export {
  EditorView,                 // Отвечает за отрисовку редактора в DOM.
  // Расширения интерфейса:
  lineNumbers,                // Номера строк слева
  highlightActiveLineGutter,  // Подсветка номера текущей строки
  highlightWhitespace,        // Подсветка обычных пробелов (точками)
  highlightTrailingWhitespace,// Подсветка пробелов в конце строк
  drawSelection,              // Отрисовка выделения текста
  highlightSpecialChars,      // Подсветка спецсимволов (NBSP, SHY и т.д.)
  keymap,                     // Обработчик горячих клавиш

  // --- УДАЛЕННЫЕ МОДУЛИ (для справки) ---
  // ViewPlugin,      // Для создания плагинов, реагирующих на изменения вида (не нужно, используем готовые)
  // Decoration,      // Для декорирования текста (цвета, виджеты) вручную (не нужно)
  // MatchDecorator,  // Для поиска и декорирования по регуляркам (используется внутри highlightSpecialChars)
  // WidgetType,      // Для вставки HTML-элементов в текст (не нужно)
  // dropCursor,      // Показывает место вставки при Drag&Drop (редактор read-only)
  // rectangularSelection, // Выделение прямоугольником (Alt+Drag) (избыточно)
  // crosshairCursor, // Курсор-перекрестие (избыточно)
} from "@codemirror/view";

// --- ЯЗЫКОВЫЕ СРЕДСТВА (Language) ---
export {
  syntaxHighlighting,     // Механизм раскраски кода
  defaultHighlightStyle,  // Стандартная цветовая схема для токенов
  bracketMatching,        // Подсветка парных скобок

  // --- УДАЛЕННЫЕ МОДУЛИ ---
  // foldGutter,      // Сворачивание кода (стрелочки слева) (не нужно для коротких текстов)
  // foldKeymap,      // Горячие клавиши для сворачивания
} from "@codemirror/language";

// --- ПОДДЕРЖКА HTML ---
// Парсер и подсветка для HTML
export { html } from "@codemirror/lang-html";

// --- КОМАНДЫ (Commands) ---
// Стандартные сочетания клавиш (стрелки, Home/End и т.д.)
export {
    defaultKeymap,

    // --- УДАЛЕННЫЕ МОДУЛИ ---
    // history,       // История изменений (Undo/Redo) (не нужно, так как read-only)
    // historyKeymap, // Горячие клавиши Ctrl+Z / Ctrl+Y
} from "@codemirror/commands";

// --- ТЕМЫ (Themes) ---
// Темная тема One Dark
export { oneDark } from "@codemirror/theme-one-dark";

// --- ДОПОЛНИТЕЛЬНО (Удалено) ---
// export { searchKeymap, highlightSelectionMatches } from "@codemirror/search"; // Поиск по тексту (Ctrl+F)
// export { autocomplete, completionKeymap } from "@codemirror/autocomplete";    // Автодополнение
// export { lintKeymap } from "@codemirror/lint";                                // Линтинг (проверка ошибок)
