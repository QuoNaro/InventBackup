# Создание резервных копий для MS SQL (Скрипт)

## Требования
- Установленный **docker и docker-compose** на вашем компьютере или сервере
- Файл `.env` в корне вашего проекта (или используйте `.env.example` для создания `.env`)

## Шаги развертывания

1. **Перейдите в корневую директорию проекта**.

2. **Создайте файл `.env`** на основе `.env.example`:
   ```bash
   cp .env.example .env
   ```

3. **Откройте файл `.env`** и заполните переменные окружения соответствующими значениями:
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


4. **Запустите контейнеры** с помощью Docker Compose:
   ```bash
   # Если сборка из исходных файлов
   docker-compose up -d --build
   ```
   Ключ `-d` запускает контейнеры в фоновом режиме.
   Также можно скачать сборку для развертывания без интернета в `Realeses`

5. **Проверьте состояние контейнеров**:
   ```bash
   docker ps
   ```

   Вы должны увидеть запущенные контейнеры вашего приложения.

## Конфигурация Docker Compose

В файле `docker-compose.yml` замените `./backup` на свою папку для резервных копий:
```yaml
version: '3'

services:
  your-app:
    # ...
    volumes:
      - ./backup:/app/BACKUP
    # ...
```
Это свяжет директорию `./backup` на локальной машине с директорией `/app/BACKUP` внутри контейнера. Вы можете изменить `./backup` на любой другой путь на локальной машине, где вы хотите хранить резервные копии.


## Дополнительные команды

- **Остановка контейнеров**:
  ```bash
  docker-compose down
  ```

- **Просмотр логов контейнеров**:
  ```bash
  docker logs container-name
  ```

  Замените `container-name` на имя нужного контейнера.

- **Вход в контейнер**:
  ```bash
  docker exec -it container-name bash
  ```

  Замените `container-name` на имя нужного контейнера.

Убедитесь, что в вашем `Dockerfile` и `docker-compose.yml` правильно указаны пути к файлам и образам. Также проверьте, что переменные окружения в `.env` соответствуют вашей конфигурации.



