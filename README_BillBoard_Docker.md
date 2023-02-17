### Запуск проекта в Docker (Django+Postgresql+Celery+Redis):  
#### Если у Вас не установлен Docker Desktop, выполните установку, следуя инструкции на [Docker Desktop](https://docs.docker.com/desktop/). Запустите приложение и проверьте его работу командой в терминале:
```
docker --version
```
#### Склонируйте проект с GitHub и перейдите в папку "BillBoard_mmorpg/billboardsite/":  
``` 
git clone https://github.com/TimurSuvorov/BillBoard_mmorpg.git && cd BillBoard_mmorpg/billboardsite/ 
```
 #### Отправка e-mail писем происходит с помощью сервиса Yandex. 
Для настройки выполните Шаг 1 и Шаг 2 по инструкции:  [Настроить программу по протоколу IMAP](https://yandex.ru/support/mail/mail-clients/others.html) . 
Сохраните пароль приложения - он понадобится на следующем шаге.

#### Переименуйте файл *`billboardsite/.env.Dockerexample`* в **`billboardsite/.env`**. Откройте его в редакторе и замените шаблонные переменные окружения:
```
yandex_EMAIL_HOST_USER = 'email_host_user' --> имя пользователя (до @ в адресе) из п.3
yandex_EMAIL_HOST_PASSWORD  = 'email_host_password' --> пароль приложения  из п.3

POSTGRES_USER = 'postgres_user' --> имя пользователя БД
POSTGRES_PASSWORD = 'postgres_password' --> пароль для доступа к БД

DJANGO_SUPERUSER_USERNAME = 'django_superuser_username' --> имя нового суперпользователя
DJANGO_SUPERUSER_EMAIL = 'django_superuser_email' --> почта нового суперпользователя (в т.ч.для добавления в группу ADMINS)
DJANGO_SUPERUSER_PASSWORD = 'django_superuser_password' --> пароль нового суперпользователя
```
#### Вернитесь в консоль и запустите Docker-compose:
```
docker-compose up
```
#### Пройдите на запущенный сервер по адресу http://127.0.0.1:8000/billboard/announcements/.
Админ-панель по адресу: http://127.0.0.1:8000/admin


