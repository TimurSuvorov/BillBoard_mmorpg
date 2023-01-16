from celery import shared_task
from django.contrib.auth.models import User, Group

from .models import Newsletter, Reply
from .utils import sendsimplemail


@shared_task
def new_user_actions_async(user_id):
    instance = User.objects.get(pk=user_id)
    sendsimplemail(subject=f'Привет {instance.username}!',
                   message=f'Привет {instance.username}! Добро пожаловать на наш сайт «MMORPG Billboard»',
                   recipient_list=[instance.email],
                   consolemessage=f'SysInfo: Отправлено письмо новому пользователю {instance.username}'
                   )

    # Добавление пользователя в группу 'common_users'
    common_group = Group.objects.get(name='common_users')
    common_group.user_set.add(instance)


@shared_task
def newsletter_mail_async(pk):
    instance = Newsletter.objects.get(pk=pk)
    all_users = User.objects.all()
    for user in all_users:
        sendsimplemail(subject=f'Новость от «MMORPG Billboard» «{instance.newsletter_preview()}»',
                       message=f'Привет {user.username}! Вышла новость «{instance.newsletter_preview()}» от наших экспертов «MMORPG Billboard»!',
                       recipient_list=[user.email],
                       consolemessage=f'SysInfo: Отправлено письмо о новости для {user.username}'
                       )


@shared_task
def reply_approved_mail_async(pk, path):
    instance = Reply.objects.get(pk=pk)
    author_ann = instance.announcement.author_ann
    sendsimplemail(subject=f'Отклик принят: «{instance.reply_preview()}»',
                   message=f'Привет {instance.author_repl}! Ваш отклик «{instance.reply_preview()}» принят пользователем {author_ann}!'
                           f'\nСсылка на Ваше объявление: {path}',
                   recipient_list=[instance.author_repl.email],
                   consolemessage=f'SysInfo: Отправлено письмо о принятии отлика для {instance.author_repl}'
                   )