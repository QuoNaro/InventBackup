#!/bin/bash

while true; do
    echo "---------------------------------------------------"
    # Удаляем файлы старше 6 месяцев
    find "/app/BACKUP/" -type f -mtime +180 -exec rm -f {} \;
    bash /app/backup-now.sh
    echo "---------------------------------------------------"
    sleep $TIMEOUT
done

