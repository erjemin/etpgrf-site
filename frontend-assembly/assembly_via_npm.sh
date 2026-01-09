#!/usr/bin/bash

# Необходимо предварительно установить NPM и esbuild:
# Для Ubuntu/Debian:
#   sudo apt install npm
#   npm install -g esbuild
# Для MacOS (через Homebrew):
#   brew install npm
#   npm install -g esbuild
# Для Windows:
#   Скачайте и установите Node.js с официального сайта: https://nodejs.org/
#   Затем установите esbuild глобально:
#   npm install -g esbuild


# Устанавливаем CodeMirror и необходимые пакеты
npm install \                                                                                                          [±main ●●]
  @codemirror/lang-html \
  @codemirror/theme-one-dark \
  @codemirror/commands \
  @codemirror/language

#  Собираем js в каталог ./public/static/codemirror/editor.js с помощью esbuild
npx esbuild src/editor.js --bundle --format=esm --outfile=../public/static/codemirror/editor.js