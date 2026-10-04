const fs = require('fs');
const path = require('path');

// Целевая папка для статики вендоров
const targetDir = path.resolve(__dirname, '../public/static/vendor');

// Список файлов и директорий для копирования
const itemsToCopy = [
  // Bootstrap 5 (CSS & JS bundle)
  {
    src: 'node_modules/bootstrap/dist/css/bootstrap.min.css',
    dest: 'bootstrap/bootstrap.min.css'
  },
  {
    src: 'node_modules/bootstrap/dist/css/bootstrap.min.css.map',
    dest: 'bootstrap/bootstrap.min.css.map'
  },
  {
    src: 'node_modules/bootstrap/dist/js/bootstrap.bundle.min.js',
    dest: 'bootstrap/bootstrap.bundle.min.js'
  },
  {
    src: 'node_modules/bootstrap/dist/js/bootstrap.bundle.min.js.map',
    dest: 'bootstrap/bootstrap.bundle.min.js.map'
  },

  // Bootstrap Icons (CSS & WOFF/WOFF2 шрифты)
  {
    src: 'node_modules/bootstrap-icons/font/bootstrap-icons.min.css',
    dest: 'bootstrap-icons/bootstrap-icons.min.css'
  },
  {
    src: 'node_modules/bootstrap-icons/font/fonts/bootstrap-icons.woff2',
    dest: 'bootstrap-icons/fonts/bootstrap-icons.woff2'
  },
  {
    src: 'node_modules/bootstrap-icons/font/fonts/bootstrap-icons.woff',
    dest: 'bootstrap-icons/fonts/bootstrap-icons.woff'
  },

  // HTMX
  {
    src: 'node_modules/htmx.org/dist/htmx.min.js',
    dest: 'htmx/htmx.min.js'
  },

  // Alpine.js
  {
    src: 'node_modules/alpinejs/dist/cdn.min.js',
    dest: 'alpinejs/cdn.min.js'
  }
];

console.log('Сборка и копирование вендорных библиотек в static/vendor/...');

let copiedCount = 0;

for (const item of itemsToCopy) {
  const srcPath = path.resolve(__dirname, item.src);
  const destPath = path.join(targetDir, item.dest);

  if (!fs.existsSync(srcPath)) {
    console.warn(`Предупреждение: исходный файл не найден: ${item.src}`);
    continue;
  }

  // Создаем папку назначения, если не существует
  const destDirPath = path.dirname(destPath);
  if (!fs.existsSync(destDirPath)) {
    fs.mkdirSync(destDirPath, { recursive: true });
  }

  fs.copyFileSync(srcPath, destPath);
  console.log(` Скопировано: ${item.src} -> ${path.relative(path.resolve(__dirname, '..'), destPath)}`);
  copiedCount++;
}

console.log(`Успешно скопировано файлов: ${copiedCount}`);
