#!/bin/bash

# Убедитесь, что вы находитесь в корневом каталоге вашего репозитория
cd "$(git rev-parse --show-toplevel)" || exit

# Функция для сохранения объектов в захэшированном виде
save_object() {
    local object_hash=$1

    # Определяем директории для сохранения объекта
    dir1="${object_hash:0:2}"  # Первые две буквы хэша
    dir2="${object_hash:2}"     # Остальная часть хэша

    # Создаем директории, если они не существуют
    mkdir -p ".git/objects/$dir1"

    # Проверяем, существует ли объект уже
    if [ ! -f ".git/objects/$dir1/$dir2" ]; then
        # Получаем объект и сохраняем его
        git cat-file -p "$object_hash" | git hash-object -w --stdin > ".git/objects/$dir1/$dir2"
        
        # Сохраняем хэш объекта в переменной
        local new_hash=$(git hash-object -w --stdin < <(git cat-file -p "$object_hash"))
        
        # Переименовываем файл в новый хэш
        mv ".git/objects/$dir1/$dir2" ".git/objects/${new_hash:0:2}/${new_hash:2}"
    fi
}

# Получаем все коммиты
git rev-list --all | while read -r commit_hash; do
    # Сохраняем объект коммита
    save_object "$commit_hash"

    # Извлекаем дерево для каждого коммита
    tree_hash=$(git rev-parse "$commit_hash^{tree}")

    # Сохраняем объект дерева
    save_object "$tree_hash"

    # Извлекаем все объекты из дерева
    git ls-tree -r "$tree_hash" | awk '{print $3}' | while read -r object_hash; do
        # Сохраняем объект блоба
        save_object "$object_hash"
    done
done

echo "Все объекты успешно извлечены в .git/objects."
