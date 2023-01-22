from celery import shared_task
from django.contrib.auth.models import User, Group
from django.core.mail import mail_admins
from django.urls import reverse_lazy, reverse

from billboardsite.settings import SITE_URL
from .models import Newsletter, Reply, UserProfile
from .utils import sendsimplemail


@shared_task
def new_user_actions_async(user_id):
    user = User.objects.get(pk=user_id)
    sendsimplemail(subject=f'Привет {user.username}!',
                   message=f'Привет {user.username}! Добро пожаловать на наш сайт «MMORPG Billboard»',
                   recipient_list=[user.email],
                   consolemessage=f'SysInfo: Отправлено письмо новому пользователю {user.username}'
                   )

    # Добавление пользователя в группу 'common_users'
    common_group = Group.objects.get(name='common_users')
    common_group.user_set.add(user)

    # Добавление профиля по умолчанию
    UserProfile.objects.get_or_create(user=user, nickname=user.username)


@shared_task
def newsletter_mail_async(pk):
    newsletter = Newsletter.objects.get(pk=pk)
    all_users = User.objects.all()
    for user in all_users:
        if user.userprofile.is_news_subscribe:
            sendsimplemail(subject=f'Новость от «MMORPG Billboard» «{newsletter.newsletter_preview()}»',
                           message=f'Привет {user.username}! Вышла новость «{newsletter.newsletter_preview()}» от наших экспертов «MMORPG Billboard»!',
                           recipient_list=[user.email],
                           consolemessage=f'SysInfo: Отправлено письмо о новости для {user.username}'
                           )
    newsletter.is_sent = True


@shared_task
def reply_approved_mail_async(pk):
    reply = Reply.objects.get(pk=pk)
    if reply.author_repl.userprofile.appr_replies_alerts:  # Настройка в профиле
        author_repl = reply.author_repl
        author_ann = reply.announcement.author_ann
        ann_local_path = reverse_lazy('announcement_detail', kwargs={'pk': reply.announcement.pk})
        sendsimplemail(subject=f'Отклик принят: «{reply.reply_preview()}»',
                       message=f'Привет {author_repl}! Ваш отклик «{reply.reply_preview()}» принят пользователем {author_ann}!'
                               f'\nСсылка на объявление: {SITE_URL}{ann_local_path}',
                       recipient_list=[author_repl.email],
                       consolemessage=f'SysInfo: Отправлено письмо о принятии отлика для {author_repl}'
                       )


@shared_task
def new_reply_mail_async(pk):
    reply = Reply.objects.get(pk=pk)
    if reply.announcement.author_ann.userprofile.is_replies_alerts:  # Настройка в профиле
        author_ann = reply.announcement.author_ann
        sendsimplemail(subject=f'Новый отклик: «{reply.reply_preview()}»',
                       message=f'Привет {author_ann}! На Ваше объявление «{reply.announcement.announcement_preview()}» оставили новый отлик!',
                       recipient_list=[author_ann.email],
                       consolemessage=f'SysInfo: Отправлено письмо о принятии отлика для {author_ann}'
                       )


@shared_task
def request_to_newsauthors_mail_async(user_id):
    user = User.objects.get(pk=user_id)
    add_local_path = reverse_lazy('add_to_newsauthors', kwargs={'user_id': user_id})
    declain_local_path = reverse_lazy('declain_to_newsauthors', kwargs={'user_id': user_id})

    mail_admins(subject=f'ЗАПРОС: Добавление в группу авторов новостей',
                message=f'Поступил запрос от {user.username} на добавление в группу авторов новостей.'
                        f'\nОдобрить: {SITE_URL}{add_local_path}'
                        f'\nОтказать: {SITE_URL}{declain_local_path}'
                )
    print(f'SysInfo: Отправлено письмо админу о добавлении в группу авторов новостей')


@shared_task
def added_to_newsauthors_mail_async(user_id):
    user = User.objects.get(pk=user_id)

    sendsimplemail(subject=f'Вы добавлены в группу авторов новостей',
                   message=f'Привет {user.username}! Вы добавлены в группу авторов новостей и теперь можете поделиться '
                           f'чем-то интересным.',
                   recipient_list=[user.email],
                   consolemessage=f'SysInfo: Отправлено письмо о добавлении в группу для {user.username}'
                   )


@shared_task
def declain_to_newsauthors_mail_async(user_id):
    user = User.objects.get(pk=user_id)
    sendsimplemail(subject=f'Отказано на добавление в группу авторов новостей',
                   message=f'Привет {user.username}! '
                           f'К сожалению, Вам отказано в запросе на добавление в группу авторов новостей',
                   recipient_list=[user.email],
                   consolemessage=f'SysInfo: Отправлено письмо с отказом на добавление в группу авторов новостей для {user.username}'
                   )
