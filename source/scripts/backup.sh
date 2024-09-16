#!/bin/sh


NAME="$PREFIX$(date +"%d-%m-%Y_%H-%M-%S").bak"
echo "Начало резервного копирования... ($(date +"%d-%m-%Y_%H:%M:%S"))"
sqlcmd -S $SERVER -U $DB_USER -P $DB_PASSWORD -C -Q "BACKUP DATABASE [$DB] TO DISK = '$WINPATH/$NAME' WITH FORMAT; " > /dev/null
echo "Файл $WINPATH/$NAME успешно создан!"

# Копирование
echo "Выполняется копирование по SSH для $WINSSH_USER@$SERVER"
sshpass -p "$WINSSH_PASSWORD" scp -o StrictHostKeyChecking=no "$WINSSH_USER@$SERVER:$WINPATH/$NAME" ./backup/
echo "Копирование файла $NAME завершено!"

# Удаление
echo "Выполняется удаление файла из $SERVER..."
sshpass -p "$WINSSH_PASSWORD" ssh -o StrictHostKeyChecking=no $WINSSH_USER@$SERVER "del $WINPATH\\$NAME"
echo "Удаление файла $WINPATH$NAME завершено!"


TAR_NAME=$PREFIX$(date +"%d-%m-%Y_%H-%M-%S").tar.xz

# Архивация

if test -e /app/backup/$NAME; then
    echo 
    echo "Файл существует. Выполняется архивация $NAME --> $TAR_NAME"
    cd ./backup/
    tar -cJf $TAR_NAME $NAME
    echo "Архивация $TAR_NAME завершено!"
    cd ..
    rm ./backup/$NAME
else
    echo "Файл не существует"
    exit 1
fi



