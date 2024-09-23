FROM fabiang/sqlcmd:latest

# Указываем рабочую директорию
WORKDIR /app

# Копируем скриптовые файлы и устанавливаем права
COPY ./scripts ./

RUN chmod +x /app/docker-entrypoint.sh
# Запуск бэкапа и начало работы cron
ENTRYPOINT ["/app/docker-entrypoint.sh"]