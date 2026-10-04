#!/usr/bin/env bash
set -e

# Переходим в директорию скрипта
cd "$(dirname "$0")"

# Необходимо предварительно установить Node.js и npm:
# Для Ubuntu/Debian:
#   sudo apt install nodejs npm
# Для MacOS (через Homebrew):
#   brew install node
# Для Windows:
#   Скачайте и установите Node.js с официального сайта: https://nodejs.org/


# Устанавливаем зависимости
npm install

# Собираем всё (CodeMirror и копирование вендорных библиотек в public/static/vendor/)
npm run build

# Подчищаем за собой node_modules
echo "Очистка node_modules..."
rm -rf node_modules