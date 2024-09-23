#!/bin/sh

# Обновление и установка пакетов
apt-get update -qq &&
apt-get install -qq -y sshpass xz-utils cron nano && 
mkdir -p ./backup/ ./logs && 

# Установка прав доступа
chmod +x /app/test.sh /app/backup.sh /app/cleanup.sh

echo "0 0 * * * /app/backup.sh >> /app/logs/cron.log 2>&1" >> /etc/crontab &&
echo "0 1 1 * * /app/cleanup.sh >> /app/logs/cron.log 2>&1" >> /etc/crontab &&
echo "*/2 * * * * /app/test.sh >> /app/logs/test.log 2>&1" >> /etc/crontab &&
crontab /etc/crontab


# Выполнить backup.sh
sh /app/backup.sh >> /app/logs/backup.log 2>&1

# Запустить cron в фоновом режиме
cron -f