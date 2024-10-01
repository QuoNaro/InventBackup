FROM alpine:latest

# Указываем рабочую директорию
WORKDIR /app

RUN mkdir /app/backup && touch backup.log

# Установка дополнительных пакетов и создание необходимых директорий
RUN apk update && apk add python3
RUN python -m venv .venv

# Копируем файлы и устанавливаем зависимости проекта
COPY . .
RUN /app/.venv/bin/pip install -r requirements.txt

RUN chmod +x docker-entrypoint.sh


# Запуск
ENTRYPOINT ["sh","./docker-entrypoint.sh"]