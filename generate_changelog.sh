#!/bin/bash

# Простой скрипт для создания changelog по требованиям

echo "=== Запуск генерации changelog ==="

# 1. Получаем версию из аргументов
if [ -z "$1" ]; then
    echo "Ошибка: Укажите версию (например: ./generate_changelog.sh v1.2.0)"
    exit 1
fi

VERSION="$1"
DATE=$(date +"%Y-%m-%d")

echo "Версия: $VERSION"
echo "Дата: $DATE"

# 2. Проверяем наличие последнего тега
LAST_TAG=$(git describe --tags --abbrev=0 2>/dev/null || echo "")

if [ -z "$LAST_TAG" ]; then
    echo "Последний тег не найден. Будут использованы все коммиты."
    COMMITS=$(git log --oneline)
else
    echo "Последний тег: $LAST_TAG"
    COMMITS=$(git log --oneline "${LAST_TAG}..HEAD")
fi

# 3. Создаем новую секцию changelog
TEMP_FILE=$(mktemp)

echo "## [$VERSION] - $DATE" >> "$TEMP_FILE"
echo "" >> "$TEMP_FILE"

# 4. Добавляем коммиты в список
if [ -z "$COMMITS" ]; then
    echo "  - Нет новых коммитов" >> "$TEMP_FILE"
else
    # Считаем количество коммитов
    COMMIT_COUNT=$(echo "$COMMITS" | wc -l)
    echo "Найдено коммитов: $COMMIT_COUNT"
    
    echo "$COMMITS" | while read line; do
        HASH=$(echo "$line" | awk '{print $1}')
        MESSAGE=$(echo "$line" | cut -d' ' -f2-)
        SHORT_HASH=${HASH:0:7}
        echo "  - $MESSAGE [$SHORT_HASH]" >> "$TEMP_FILE"
    done
fi

echo "" >> "$TEMP_FILE"

# 5. Добавляем новую версию в начало файла CHANGELOG.md
if [ -f "CHANGELOG.md" ]; then
    echo "Обновляю существующий CHANGELOG.md..."
    cat "$TEMP_FILE" CHANGELOG.md > CHANGELOG_NEW.md
    mv CHANGELOG_NEW.md CHANGELOG.md
else
    echo "Создаю новый CHANGELOG.md..."
    echo "# Changelog" > CHANGELOG.md
    echo "" >> CHANGELOG.md
    echo "Все изменения в проекте." >> CHANGELOG.md
    echo "" >> CHANGELOG.md
    cat "$TEMP_FILE" >> CHANGELOG.md
fi

# 6. Создаем тег (опционально, но по требованиям)
echo "Создаю тег $VERSION..."
git tag -a "$VERSION" -m "Release $VERSION" 2>/dev/null || echo "Тег уже существует или ошибка создания"

# 7. Убираем временный файл
rm "$TEMP_FILE"

echo "=== Готово! ==="
echo "Changelog создан: CHANGELOG.md"
echo "Просмотр первых строк:"
head -20 CHANGELOG.md