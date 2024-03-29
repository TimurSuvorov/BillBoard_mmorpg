﻿

# BillBoard_MMORPG Site  
### Техническое задание и общая информация о проекте  
В рамках проекта был реализован информационный интернет-ресурс, который может послужить прототипом для других аналогичных проектов. В данном случае  - для фанатов игры MMORPG.    
В проекте реализована возможность размещения категоризированных объявлений-заданий и комментариев к ним для зарегистрированных пользователей. На каждый комментарий автор объявления может реагировать - принимать, отклонять и сбрасывать статус.  

### Функционал: 
Фронтенд оформление взято из шаблонов и адаптирована "под себя".

*Имплементация и используемые инструменты:*
- фреймворк Django;  
- хранение данных - PostgreSQL;  
- регистрация/авторизация через email или социальные сети - allauth (подтверждение через 6-значный OTP);  
- асинхронное выполнение задач по e-mail рассылке* и др. - Celery+Redis; 
- обработка фотоконтента перед сохранением на сервер - библиотека Pillow;
- встроенный WYSIWYG-редактор - CKEditor;
- оптимизация сайта - Django Debug Toolbar;

*Сейчас активированы следующие e-mail оповещения-рассылки, которые выполняются асинхронно:  
  
 - **для пользователей сайта** ( [*] - с возможностью отключения в профиле пользователя):  
   - на приветствие при регистрации и подтверждении аккаунта[*];  
   - на размещение нового отлика для объявления его автору[*];  
   - на публикацию статьи в новостной ленте[*];  
   - на добавление/отклонение в группу авторов статей инициатору заявки;  
    
 - **для администраторов и модераторов сайта:**  
    - запрос от пользователя на возможность размещения статей в ленте;  

***  
### Развертывание проекта:  
  Развертывание проекта можно произвести с помощью [Docker](https://github.com/TimurSuvorov/BillBoard_mmorpg/blob/master/README_BillBoard_Docker.md) или [на пользовательской системе](https://github.com/TimurSuvorov/BillBoard_mmorpg/blob/master/README_BillBoard_UserSystem.md).
 
