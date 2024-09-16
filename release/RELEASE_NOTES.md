# Инструкция для развертывания без интернета

## 📥 Шаг 1: Скачивание образа 
Скачайте локальный [образ Docker](https://github.com/QuoNaro/mssql-duplica-script/releases) актуальной версии 
## 📦 Шаг 2: Разархивируйте образ
```bash
unzip mssql-duplica-script.zip
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

Перед запуском приложения вам необходимо изменить файл `.env` в корне проекта. Откройте файл `.env.example` в текстовом редакторе и настройте необходимые параметры, такие как:
### Пример конфигурации
```env
 # Путь для резервного копирования внутри Windows Server
 WINPATH=C:\backup\

 # Пароль для SSH-доступа к Windows-серверу
 WINSSH_PASSWORD=your_password_here

 # Имя пользователя для SSH-доступа к Windows-серверу
 WINSSH_USER=your_username_here

 # IP-адрес сервера базы данных
 SERVER=127.0.0.1

 # Имя базы данных для MS SQL Server
 DB=test_db

 # Имя пользователя для подключения к базе данных MS SQL Server
 DB_USER=your_db_user_here

 # Пароль для подключения к базе данных MS SQL Server
 DB_PASSWORD=your_db_password_here

 # Префикс названия бэкапа
 PREFIX=inv
```

Нужно переименновать файл `.env.example` в `.env`
```bash
mv .env.example .env
```

## 🚀 Шаг 5: Запуск приложения

Теперь, когда все готово, вы можете запустить приложение с помощью Docker Compose. Выполните следующую команду:

```bash
docker-compose up -d
```
Эта команда запустит ваше приложение в фоновом режиме.
