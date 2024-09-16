FROM fabiang/sqlcmd:latest

# Указываем рабочую директорию
WORKDIR /app

# Установка дополнительных пакетов и создание необходимых директорий
RUN apt-get update -qq && \
    apt-get install -qq -y sshpass xz-utils cron nano && \
    mkdir -p ./backup/ ./logs && \
    rm -rf /var/lib/apt/lists/*

# Копируем скриптовые файлы и устанавливаем права
COPY ./scripts ./
RUN chmod +x ./backup.sh ./cleanup.sh ./docker-entrypoint.sh

# Настройка cron
RUN echo "0 0 * * * /app/backup.sh /app/logs/cron.log 2>&1" >> /etc/crontab && \
    echo "0 1 1 * * /app/cleanup.sh /app/logs/cron.log 2>&1" >> /etc/crontab && \
    crontab /etc/crontab

# Запуск бэкапа и начало работы cron
ENTRYPOINT ["/app/docker-entrypoint.sh"]