// Реэкспорт всех необходимых модулей для использования в браузере (через <script type="module">)

export { EditorState } from "@codemirror/state";
export {
  EditorView,
  lineNumbers,
  highlightActiveLineGutter,
  highlightWhitespace,
  highlightTrailingWhitespace,
  drawSelection,
  highlightSpecialChars,
  keymap,
  ViewPlugin,
  Decoration,
  MatchDecorator,
  WidgetType
} from "@codemirror/view";

export {
  syntaxHighlighting,
  defaultHighlightStyle,
  bracketMatching
} from "@codemirror/language";

export { html } from "@codemirror/lang-html";
export { defaultKeymap, history, historyKeymap } from "@codemirror/commands";
export { oneDark } from "@codemirror/theme-one-dark";

// Можно оставить и фабрику, если пригодится для быстрого старта
export function createReadOnlyEditor(parent, text) {
  // ... (код фабрики можно оставить или убрать, он не мешает)
}
