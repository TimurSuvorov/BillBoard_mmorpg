﻿# Настройка PostgreSQL

В проекте используется БД PostgreSQL. Ниже приведены инструкции для установки и настройки БД, апробированные на Ubuntu 20.04 LTS.

**1. Установка и запуск PostgreSQL**
##### Обновляем список пакетов OS и устанавливаем PostgreSQL вместе с пакетом -contrib:
     sudo apt update
     sudo apt install postgresql postgresql-contrib
##### Запуск сервер PostgreSQL и проверка статуса:
     sudo service postgresql start
     service postgresql status
     >> 12/main (port 5432): online

**2. Создание пользователя и базы данных**
##### Выполним вход в консоль от имени пользователя "postgres":
     sudo -u postgres psql
##### Посмотрим статус подключения, проверив, что Вы на верном пути:
     \conninfo
    >>> You are connected to database "postgres" as user "postgres" via socket in "/var/run/postgresql" at port "5432".
   ##### Создадим БД *billboardsite_db* для проекта:

    CREATE DATABASE billboardsite_db; 
   ##### Создадим пользователя базы данных для подключения и взаимодействия с БД и применим необходимые настройки (вместо *postgres_user* и *postgres_password* подставьте свои значения):

     CREATE USER postgres_user WITH PASSWORD 'postgres_password';
     ALTER ROLE postgres_user SET client_encoding TO 'utf8';
     ALTER ROLE postgres_user SET default_transaction_isolation TO 'read committed'; 
     ALTER ROLE postgres_user SET timezone TO 'UTC';
     GRANT ALL PRIVILEGES ON DATABASE myproject TO postgres_user;

**3. Настройка со стороны Django в IDE**
##### В файле *billboardsite/settings.py* удалите настройки по умолчанию DATABASES для SQLite3:
    # setting.py
        DATABASES = {  
        'default': {  
            'ENGINE': 'django.db.backends.postgresql_psycopg2',  
	        'NAME': 'billboardsite_db',  
	        'USER': os.getenv('POSTGRES_USER'),  
		    'PASSWORD': os.getenv('POSTGRES_PASSWORD'),  
	        'HOST': 'localhost',  
	        'PORT': '5432',  
		    }  
        }
   
##### Измените имя файла "*.env.example*" на "*.env.*" в billboardsite/. Замените шаблонные значения POSTGRES_USER  и POSTGRES_PASSWORD для загрузки их в среду окружения переменных при запуске:
    # .env
	    POSTGRES_USER = 'postgres_user'  
	    POSTGRES_PASSWORD = 'postgres_password'
##### Перейдите в консоль. Убедитесь, что Вы находитесь в созданном ранее виртуальном окружении. Выполните команды на создание и применение миграций:    
    python manage.py makemigrations
    python manage.py migrate
##### Удалите **content types** для исключения инконсистенций в будущем:    
    python manage.py shell
    from django.contrib.contenttypes.models import ContentType
    ContentType.objects.all().delete()
    quit()

##### (опционально)  Загрузка дампа БД

    python manage.py loaddata db_billboard.json