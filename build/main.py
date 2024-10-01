import pymssql
import os
from pathlib import Path
import datetime
import tarfile
import paramiko
import sys
from loguru import logger






class ConnectionError(Exception):
    pass

def get_filename(prefix: str, ext: str = None) -> str:
        current_time = datetime.datetime.now().strftime("%d-%m-%Y__%H-%M-%S")
        filename = f"{prefix}_{current_time}"
        if ext:
            filename = f'{filename}.{ext}'
        return filename

class DatabaseBackup:
    def __init__(self, server: str, user: str, password: str, database: str):
        self.server = server
        self.user = user
        self.password = password
        self.database = database

    def backup(self, filepath: str):
        conn = pymssql.connect(server=self.server, user=self.user, password=self.password, database=self.database, as_dict=True)
        
        try:
            cursor = conn.cursor()
            SQL_TEST_QUERY = """SELECT name FROM sys.databases"""
            cursor.execute(SQL_TEST_QUERY)
            
            if not ({'name': self.database} in cursor):
                logger.error('Ошибка подключения к БД')
                raise ConnectionError('Ошибка подключения к БД')
            else:
                logger.info(f'Успешное подключение к {self.server}')

            conn.autocommit(True)

            SQL_BACKUP_QUERY = f"""BACKUP DATABASE [{self.database}] TO DISK = '{filepath}' WITH FORMAT"""
            cursor.execute(SQL_BACKUP_QUERY)
            logger.info(f'Резервное копирование базы данных {self.database} завершено успешно.')
        
        except pymssql.DatabaseError as e:
            logger.error(f'Ошибка при выполнении резервного копирования: {e}')
        
        finally:
            cursor.close()
            conn.close()

class SSHConnection:
    def __init__(self, host: str, username: str, password: str, port=22):
        self.transport = paramiko.Transport((host, port))
        self.transport.connect(username=username, password=password)
        self.sftp = paramiko.SFTPClient.from_transport(self.transport)
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh.connect(hostname=host, username=username, password=password)

    def get(self, remote_path: str, local_path: str):
        self.sftp.get(remote_path, local_path)

    def rm_remote_file(self, remote_file: str):
        stdin, stdout, stderr = self.ssh.exec_command(f'del {remote_file}')

    def close(self):
        self.sftp.close()
        self.transport.close()
        self.ssh.close()

class Archiver:
    @staticmethod
    def archive(output_filename: str, local_file: str):
        with tarfile.open(output_filename, "w:xz") as tar:
            tar.add(local_file, arcname=os.path.basename(local_file))

def backup(config : dict):
    FILENAME = get_filename(prefix=config["PREFIX"], ext='bak')
    REMOTEFILEPATH = f"{config['REMOTEPATH']}{FILENAME}"
    LOCALFILEPATH  = f"{config['LOCALPATH']}{FILENAME}"

    db_backup = DatabaseBackup(server=config['HOST'], user=config["DB_USER"], password=config["DB_PASSWORD"], database=config["DB"])
    db_backup.backup(REMOTEFILEPATH)

    # Создание SSH соединения
    logger.info(f"Попытака SSH-подключения к {config['HOST']}")
    ssh_connection = SSHConnection(host=config['HOST'], username=config["WINSSH_USER"], password=config['WINSSH_PASSWORD'])
    logger.info('Подключение успешно!')
    # Копирование файла 
    logger.info('Копирование файла...')
    ssh_connection.get(remote_path=REMOTEFILEPATH, local_path=LOCALFILEPATH)
    logger.info(f'Файл скопирован из {config["HOST"]}:{REMOTEFILEPATH} в {LOCALFILEPATH}')

    # Удаление удалённого файла
    logger.info('Удаление файла..')
    ssh_connection.rm_remote_file(REMOTEFILEPATH)
    ssh_connection.close()
    logger.info('Удаление файла успшно!')


    # Архивирование файла 
    logger.info('Архивирование файла...')
    Archiver.archive(output_filename=f'{LOCALFILEPATH}.tar.xz', local_file=LOCALFILEPATH)
    logger.info(f'Архивирование успешно!')
    
    # Удаление файла вне архива 
    os.remove(LOCALFILEPATH)

def main():
    
    
    # Удаляем стандартный обработчик
    logger.remove()
    # Добавляем обработчик для вывода в консоль
    form = "| {level} | {time:YYYY-MM-DD} | {time:HH:mm:ss} | {message}"
    logger.add(sys.stdout, format=form)
    # Добавляем обработчик для первого файла
    logger.add("backup.log", format=form)

    # from dotenv import dotenv_values
    config = {
      "HOST" : os.getenv("HOST"),
      "WINSSH_PASSWORD" : os.getenv("WINSSH_PASSWORD"),
      "WINSSH_USER": os.getenv("WINSSH_USER"),
      "DB" : os.getenv("DB"),
      "DB_USER" : os.getenv("DB_USER"),
      "DB_PASSWORD" : os.getenv("DB_PASSWORD"),
      "PREFIX" : os.getenv("PREFIX"),
      "REMOTEPATH" : os.getenv("REMOTEPATH"),
      "LOCALPATH" : os.getenv("LOCALPATH")}
    #config = dict(dotenv_values('.env'))
    backup(config)

def start():
    import schedule
    import time

    # Запланировать выполнение функции каждый день в 00:00
    schedule.every().day.at("00:00").do(main)
    # schedule.every().minute.do(main)
    while True:
        schedule.run_pending()
        time.sleep(10)


if __name__ == '__main__':
    main()
    start()