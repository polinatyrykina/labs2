#!/bin/bash

# Скрипт для создания changelog в GitHub Actions
# Автоматически определяет версию из тега

echo "=== Генерация changelog ==="

# 1. Определяем версию из окружения GitHub Actions
if [ -n "$GITHUB_REF_NAME" ]; then
    VERSION="$GITHUB_REF_NAME"
    echo "Версия из GitHub: $VERSION"
else
    # Если запускаем локально, используем дату
    VERSION="v$(date +'%Y.%m.%d')"
    echo "Локальная версия: $VERSION"
fi

DATE=$(date +"%Y-%m-%d")
echo "Дата: $DATE"

# 2. Получаем предыдущий тег для сравнения
echo "Ищу предыдущие теги..."
ALL_TAGS=$(git tag --sort=-v:refname)

if [ -z "$ALL_TAGS" ]; then
    echo "Других тегов нет. Беру все коммиты."
    COMMITS=$(git log --oneline --reverse)
else
    # Ищем предыдущий тег (второй в списке после текущего)
    PREV_TAG=$(echo "$ALL_TAGS" | grep -A1 "^$VERSION$" | tail -1)
    
    if [ -z "$PREV_TAG" ] || [ "$PREV_TAG" = "$VERSION" ]; then
        # Если это первый тег или не нашли предыдущий
        PREV_TAG=$(echo "$ALL_TAGS" | head -1)
    fi
    
    if [ "$PREV_TAG" = "$VERSION" ]; then
        echo "Это первый тег. Беру все коммиты."
        COMMITS=$(git log --oneline --reverse)
    else
        echo "Предыдущий тег: $PREV_TAG"
        COMMITS=$(git log --oneline --reverse "${PREV_TAG}..HEAD")
    fi
fi

# 3. Создаем секцию changelog
echo "Создаю changelog..."
{
    echo "## [$VERSION] - $DATE"
    echo ""
    
    if [ -z "$COMMITS" ]; then
        echo "  - Нет изменений"
    else
        echo "$COMMITS" | while read line; do
            HASH=$(echo "$line" | awk '{print $1}')
            MSG=$(echo "$line" | cut -d' ' -f2-)
            echo "  - $MSG [${HASH:0:7}]"
        done
    fi
    echo ""
} > new_changelog.txt

# 4. Добавляем в CHANGELOG.md
if [ -f "CHANGELOG.md" ]; then
    echo "Обновляю существующий CHANGELOG.md"
    cat new_changelog.txt CHANGELOG.md > CHANGELOG_NEW.md
    mv CHANGELOG_NEW.md CHANGELOG.md
else
    echo "Создаю новый CHANGELOG.md"
    echo "# Changelog" > CHANGELOG.md
    echo "" >> CHANGELOG.md
    echo "История изменений проекта." >> CHANGELOG.md
    echo "" >> CHANGELOG.md
    cat new_changelog.txt >> CHANGELOG.md
fi

# 5. Очистка
rm new_changelog.txt

echo "=== Готово! ==="
echo "Создан CHANGELOG.md для версии $VERSION"