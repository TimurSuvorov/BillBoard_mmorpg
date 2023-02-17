### Запуск проекта в системе пользователя:  
  
 #### Склонируйте проект с GitHub локально и перейдите в папку "BillBoard_mmorpg":  
```  
git clone https://github.com/TimurSuvorov/BillBoard_mmorpg.git && cd BillBoard_mmorpg  
```  
 #### Создайте виртуальное окружение для проекта и установите необходимые пакеты из файла *billboardsite/requirements.txt*:  
```  
python3 -m virtualenv venvBillboard  
source venvBillboard/bin/activate  
pip install -r billboardsite/requirements.txt  
```  
 #### Установите сервер **Redis** в Вашей OS:  
```  
sudo apt-get update  
sudo apt-get install redis  
```  
 #### Произведите установку и настройку **PostgreSQL** [по инструкции](./README_PostgreSQL.md)  
 #### Отправка e-mail писем происходит с помощью сервиса Yandex. 
Для настройки выполните Шаг 1 и Шаг 2 по инструкции:  [Настроить программу по протоколу IMAP](https://yandex.ru/support/mail/mail-clients/others.html) . 
Сохраните пароль приложения - он понадобится на следующем шаге.
 #### В файле *billboardsite/.env* замените шаблонные переменные окружения:
```
yandex_EMAIL_HOST_USER = 'email_host_user' --> имя пользователя (до @ в адресе) из п.3
yandex_EMAIL_HOST_PASSWORD  = 'email_host_password' --> пароль приложения  из п.3
```
 #### Теперь запустите всё необходимое в отдельных консольных окнах: 
	 - `redis-server` - сервер Redis:  
	 - `sudo service postgresql start` - сервер PostgreSQL <sub>(уже должен запущен)</sub>
	 - `celery -A billboardsite worker -l INFO` -  воркер Celery из каталога проекта *billboardsite/* [^*]  
	 - `python manage.py runserver` - запуск Django-проекта из каталога проекта *billboardsite/* [^*]

[^*]: убедитесь, что у Вас активировано виртуальное окружение
