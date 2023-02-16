### Запуск проекта в системе пользователя:  
  
 1. Склонируйте проект с GitHub локально и перейдите в папку "BillBoard_mmorpg":  
```  
git clone https://github.com/TimurSuvorov/BillBoard_mmorpg.git && cd BillBoard_mmorpg  
```  
 2. Создайте виртуальное окружение для проекта и установите необходимые пакеты из файла *billboardsite/requirements.txt*:  
```  
python3 -m virtualenv venvBillboard  
source venvBillboard/bin/activate  
pip install -r billboardsite/requirements.txt  
```  
 3. Установите сервер **Redis** в Вашей OS:  
```  
sudo apt-get update  
sudo apt-get install redis  
```  
 4. Произведите установку и настройку **PostgreSQL** [по инструкции](https://github.com/TimurSuvorov/BillBoard_mmorpg/blob/master/README_PostgreSQL.md)  
 5. В файле *billboardsite/.env* замените шаблонное значение *django_secret_key* - на уникальный ключ  
 6. Отправка e-mail писем происходит с помощью Yandex. Для этого:  
    - выполните предварительные настройки: https://yandex.ru/support/mail/mail-clients/others.html  
    - в файле *billboardsite/.env* замените шаблонные значения:  
       - *yandex_EMAIL_HOST_USER* - имя пользователя (до @ в адресе)  
       - *yandex_EMAIL_HOST_PASSWORD* - пароль приложения  
 7. Теперь запустите всё необходимое в отдельных консольных окнах: 
	-  `redis-server` - сервер Redis:  
	 - `sudo service postgresql start` - сервер PostgreSQL <sub>(уже должен запущен)</sub>
	 - `celery -A billboardsite worker -l INFO` - [!] воркер Celery из каталога проекта *billboardsite/*  
	 - `python manage.py runserver` - [!] запуск Django-проекта из каталога проекта *billboardsite/* 

*[!] - убедитесь, что у Вас активировано виртуальное окружение
