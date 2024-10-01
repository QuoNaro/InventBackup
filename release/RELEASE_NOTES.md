# Инструкция для развертывания без интернета

## 📥 Шаг 1: Скачивание образа 
Скачайте локальный [образ Docker](https://github.com/QuoNaro/mssql-duplica-script/releases) актуальной версии 
## 📦 Шаг 2: Разархивируйте образ
```bash
unzip mds*.zip
```
## 🛠️ Шаг 3: Загрузка Docker-образа

1. Сделайте файл `load.sh` исполняемым:

```bash
chmod +x load.sh
```

2. Выполните скрипт для загрузки образа в Docker:

```bash
./load.sh
```
## 🔧 Шаг 4: Настройка конфигурации

Перед запуском приложения вам необходимо изменить файл `.env` в корне проекта. Откройте файл `.env` в текстовом редакторе и настройте необходимые параметры, такие как:
### Пример конфигурации
```env
    # MAIN
    HOST=172.16.62.151
    PREFIX=backup

    # SSH
    WINSSH_PASSWORD=CtrDotKem#1
    WINSSH_USER=admin

    # DATABASE
    DB=db
    DB_USER=db_user
    DB_PASSWORD=sa

    # PATH
    REMOTEPATH=C:\windows\path\to\backup\
    LOCALPATH=/path/to/backups/

    ```

## 🚀 Шаг 5: Запуск приложения

Теперь, когда все готово, вы можете запустить приложение с помощью Docker Compose. Выполните следующую команду:

```bash
docker-compose up -d
```
Эта команда запустит ваше приложение в фоновом режиме.
