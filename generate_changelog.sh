#!/bin/bash

# Простейший скрипт для changelog

echo "Создаю простой changelog..."

# Просто создаем файл с текущей датой
echo "# Changelog" > CHANGELOG.md
echo "" >> CHANGELOG.md
echo "## [v1.0.0] - $(date +'%Y-%m-%d')" >> CHANGELOG.md
echo "  - Проект создан" >> CHANGELOG.md
echo "" >> CHANGELOG.md

echo "Готово! Создан CHANGELOG.md"