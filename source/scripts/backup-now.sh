#!/bin/bash


NAME="$PREFIX$(date +"%d-%m-%Y").bak"
echo "Начало резервного копирования... ($(date +"%d-%m-%Y_%H:%M:%S"))"
sqlcmd -S $SERVER -U $DB_USER -P $DB_PASSWORD -C -Q "BACKUP DATABASE [$DB] TO DISK = '$WINPATH/$NAME' WITH FORMAT; " > /dev/null
echo "Файл $WINPATH/$NAME успешно создан!"

# Копирование
echo "Выполняется копирование по SSH для $WINSSH_USER@$SERVER"
sshpass -p "$WINSSH_PASSWORD" scp -o StrictHostKeyChecking=no "$WINSSH_USER@$SERVER:$WINPATH/$NAME" ./BACKUP/
echo "Копирование файла $NAME завершено!"

# Удаление
echo "Выполняется удаление файла из $SERVER..."
sshpass -p "$WINSSH_PASSWORD" ssh -o StrictHostKeyChecking=no $WINSSH_USER@$SERVER "del $WINPATH\\$NAME"
echo "Удаление файла $WINPATH$NAME завершено!"


TAR_NAME=$PREFIX$(date +"%d-%m-%Y").tar.xz

# Архивация
echo "Выполняется архивация $NAME --> $TAR_NAME"
cd ./BACKUP/
tar -cJf $TAR_NAME $NAME
echo "Архивация $TAR_NAME завершено!"
cd ..
rm ./BACKUP/$NAME

