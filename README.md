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
    # MAIN
    HOST=172.16.62.151

    # SSH

    WINSSH_PASSWORD=CtrDotKem#1
    WINSSH_USER=admin

    # DATABASE
    DB=db
    DB_USER=db_user
    DB_PASSWORD=sa
    PREFIX=backup

    # PATH
    REMOTEPATH=C:\windows\path\to\backup\
    LOCALPATH=/path/to/backups/

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
      - ./backup:/app/backup
    # ...
```
Это свяжет директорию `./backup` на локальной машине с директорией `/app/backup` внутри контейнера. Вы можете изменить `./backup` на любой другой путь на локальной машине, где вы хотите хранить резервные копии.


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



