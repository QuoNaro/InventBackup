FROM fabiang/sqlcmd:latest

# Указываем рабочую директорию
WORKDIR /app

# Установка дополнительных пакетов
RUN apt update > /dev/null && apt install -y sshpass xz-utils > /dev/null

# Копируем скриптовые файлы
COPY ./scripts ./

ARG WINPATH
ARG SERVER
ARG DB
ARG DB_USER
ARG DB_PASSWORD
ARG WINSSH_PASSWORD
ARG WINSSH_USER

ENV WINPATH=${WINPATH} \
    SERVER=${SERVER} \
    DB=${DB} \
    DB_USER=${DB_USER} \
    DB_PASSWORD=${DB_PASSWORD} \
    WINSSH_PASSWORD=${WINSSH_PASSWORD} \
    WINSSH_USER=${WINSSH_USER} \
    PREFIX=${PREFIX}

# Создаём папку для бэкапов внутри контейнера
RUN mkdir ./BACKUP/



# Тестирование
RUN chmod +x /app/backup.sh
RUN chmod +x /app/backup-now.sh

ENTRYPOINT ["/app/backup.sh"]

