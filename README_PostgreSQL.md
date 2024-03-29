﻿# Настройка PostgreSQL

В проекте используется БД PostgreSQL. Ниже приведены инструкции для установки и настройки БД, апробированные на Ubuntu 20.04 LTS.

# Настройка PostgresSQL  
  
В проекте используется БД PostgreSQL. Ниже приведены инструкции для установки и настройки БД, апробированные на Ubuntu 20.04 LTS.  
  
**1. Установка и запуск PostgreSQL**  
##### Обновляем список пакетов OS и устанавливаем PostgreSQL вместе с пакетом -contrib:  
```
sudo apt update sudo apt install postgresql postgresql-contrib
```

 ##### Запуск сервер PostgreSQL и проверка статуса: 
 ```
sudo service postgresql start 
service postgresql status 
>> 12/main (port 5432): online
```

**2. Создание пользователя и базы данных**  
##### Выполним вход в консоль от имени пользователя "postgres": 
```
sudo -u postgres psql
 ```
 ##### Посмотрим статус подключения, проверив, что Вы на верном пути: 
 ```
\conninfo 
 >>> You are connected to database "postgres" as user "postgres" via socket in "/var/run/postgresql" at port "5432".  
 ```
 ##### Создадим БД *billboardsite_db* для проекта:  
  ```
 CREATE DATABASE billboardsite_db; 
 ```
 ##### Создадим пользователя базы данных для подключения и взаимодействия с БД и применим необходимые настройки (вместо *postgres_user* и *postgres_password* подставьте свои значения):  
  ```
 CREATE USER postgres_user WITH PASSWORD 'postgres_password'; 
 ALTER ROLE postgres_user SET client_encoding TO 'utf8'; 
 ALTER ROLE postgres_user SET default_transaction_isolation TO 'read committed'; 
 ALTER ROLE postgres_user SET timezone TO 'UTC';  
 GRANT ALL PRIVILEGES ON DATABASE billboardsite_db TO postgres_user; 
 ```
**3. Настройка со стороны Django в IDE и изменение переменных окружения**  
##### В файле *billboardsite/settings.py* убедитесь верности настройки блока DATABASES: 
```
	 # setting.py 
DATABASES = {  
    'default': {  
		  'ENGINE': 'django.db.backends.postgresql_psycopg2',  
		  'NAME': os.getenv('POSTGRES_DB', default='billboardsite_db'),  
		  'USER': os.getenv('POSTGRES_USER'),  
		  'PASSWORD': os.getenv('POSTGRES_PASSWORD'),  
		  'HOST': os.getenv('POSTGRES_HOST', default='localhost'),  
		  'PORT': '5432',  
		  }  
    }
  ```
  ##### Измените имя файла "*.env.UserSystemexample*" на "*.env.*" в billboardsite/. Замените шаблонные значения переменных окружения POSTGRES_USER и POSTGRES_PASSWORD: 
  ```
	 # .env 
 POSTGRES_USER = 'postgres_user'       
 POSTGRES_PASSWORD = 'postgres_password' 
 ```
##### Перейдите в консоль. Убедитесь, что Вы находитесь в созданном ранее виртуальном окружении. Выполните команды на создание и применение миграций: 
```
 python manage.py makemigrations 
 python manage.py migrate
 ```
 ##### Удалите содержимое таблицы **content types** для исключения инконсистенций при загрузке дампа БД:
 ```
 python manage.py shell 
 from django.contrib.contenttypes.models 
 import ContentType 
 ContentType.objects.all().delete() 
 quit()
 ```
##### Загрузка дампа БД _"db_postgres_billboard.json"_  
  ```
 python manage.py loaddata db_postgres_billboard.json
 ```
##### Продолжите выполнение основной [инструкции](./README_BillBoard_UserSystem.md#отправка-e-mail-писем-происходит-с-помощью-сервиса-yandex)
