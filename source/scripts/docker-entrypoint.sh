#!/bin/sh

# Выполнить backup.sh
sh /app/backup.sh >> /app/logs/backup.log 2>&1

# Запустить cron в фоновом режиме
cron -f