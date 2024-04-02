#!/bin/bash

# Получить путь к папке, содержащей этот скрипт
SCRIPT_DIR=$(dirname "$0")

# Создайте файл pu
echo '#!/usr/bin/env python3' > "$SCRIPT_DIR/pu"

# Добавьте содержимое вашего pu.py в файл pu
cat "$SCRIPT_DIR/pu.py" >> "$SCRIPT_DIR/pu"

# Сделайте файл исполняемым
chmod +x "$SCRIPT_DIR/pu"

# Переместите файл pu в системный путь
sudo mv "$SCRIPT_DIR/pu" /usr/local/bin/

# Проверьте, что pu доступен глобально
if command -v pu &> /dev/null; then
    echo "The 'pu' command is now available."
else
    echo "The 'pu' command could not be installed."
fi