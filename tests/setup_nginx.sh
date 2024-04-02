#!/bin/bash

# Путь к каталогу, где хранятся файлы конфигурации Nginx
NGINX_CONF_DIR="/etc/nginx"

# Путь к каталогу, где хранятся доступные конфигурации сайтов
SITES_AVAILABLE="$NGINX_CONF_DIR/sites-available"

# Путь к каталогу, где хранятся включенные конфигурации сайтов
SITES_ENABLED="$NGINX_CONF_DIR/sites-enabled"

# Проверяем, установлен ли Nginx
if ! command -v nginx &> /dev/null; then
    echo "Nginx не установлен. Установка..."
    # Установка Nginx (пример для Ubuntu, для CentOS используйте yum)
    sudo apt-get update
    sudo apt-get install -y nginx
else
    echo "Nginx уже установлен."
fi

# Останавливаем Nginx
echo "Остановка Nginx..."
sudo systemctl stop nginx

# Удаляем существующие файлы конфигурации
echo "Удаление существующих файлов конфигурации..."
sudo rm -rf $SITES_AVAILABLE/*
sudo rm -rf $SITES_ENABLED/*

# Создаем каталоги для конфигураций
echo "Создание каталогов для конфигураций..."
sudo mkdir -p $SITES_AVAILABLE
sudo mkdir -p $SITES_ENABLED

# Создаем новый файл конфигурации для порта 80
echo "Создание конфигурации для порта 80..."
echo "server {
    listen 80 default_server;
    server_name _;
    location / {
        root /var/www/html80;
        index index.html;
    }
}" | sudo tee $SITES_AVAILABLE/port80.conf > /dev/null

# Создаем символическую ссылку для включения конфигурации
sudo ln -sf $SITES_AVAILABLE/port80.conf $SITES_ENABLED/

# Создаем новый файл конфигурации для порта 90
echo "Создание конфигурации для порта 90..."
echo "server {
    listen 90;
    server_name _;
    location / {
        root /var/www/html90;
        index index.html;
    }
}" | sudo tee $SITES_AVAILABLE/port90.conf > /dev/null

# Создаем символическую ссылку для включения конфигурации
sudo ln -sf $SITES_AVAILABLE/port90.conf $SITES_ENABLED/

# Создаем каталоги для страниц
echo "Создание каталогов для страниц..."
sudo mkdir -p /var/www/html80
sudo mkdir -p /var/www/html90

# Создаем дефолтные страницы
echo "<html><body><h1>Welcome to port 80</h1></body></html>" | sudo tee /var/www/html80/index.html > /dev/null
echo "<html><body><h1>Welcome to port 90</h1></body></html>" | sudo tee /var/www/html90/index.html > /dev/null

# Проверяем конфигурацию Nginx
echo "Проверка конфигурации Nginx..."
if ! sudo nginx -t; then
    echo "Ошибка в конфигурации Nginx. Исправьте ошибки и повторите попытку."
    exit 1
fi

# Перезапускаем Nginx
echo "Перезапуск Nginx..."
sudo systemctl start nginx

echo "Nginx успешно обновлен и перезапущен с двумя конфигурациями на портах 80 и 90."