from celery import shared_task
from django.contrib.auth.models import User, Group
from django.urls import reverse_lazy, reverse

from billboardsite.settings import SITE_URL
from .models import Newsletter, Reply
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


@shared_task
def newsletter_mail_async(pk):
    newsletter = Newsletter.objects.get(pk=pk)
    all_users = User.objects.all()
    for user in all_users:
        sendsimplemail(subject=f'Новость от «MMORPG Billboard» «{newsletter.newsletter_preview()}»',
                       message=f'Привет {user.username}! Вышла новость «{newsletter.newsletter_preview()}» от наших экспертов «MMORPG Billboard»!',
                       recipient_list=[user.email],
                       consolemessage=f'SysInfo: Отправлено письмо о новости для {user.username}'
                       )
    newsletter.is_sent = True


@shared_task
def reply_approved_mail_async(pk):
    reply = Reply.objects.get(pk=pk)
    author_ann = reply.announcement.author_ann
    author_repl = reply.author_repl
    ann_local_path = reverse_lazy('announcement_detail', kwargs={'pk': reply.announcement.pk})
    sendsimplemail(subject=f'Отклик принят: «{reply.reply_preview()}»',
                   message=f'Привет {author_repl}! Ваш отклик «{reply.reply_preview()}» принят пользователем {author_ann}!'
                           f'\nСсылка на Ваше объявление: {SITE_URL}{ann_local_path}',
                   recipient_list=[author_repl.email],
                   consolemessage=f'SysInfo: Отправлено письмо о принятии отлика для {author_repl}'
                   )


@shared_task
def new_reply_mail_mail_async(pk):
    reply = Reply.objects.get(pk=pk)
    author_ann = reply.announcement.author_ann
    sendsimplemail(subject=f'Новый отклик: «{reply.reply_preview()}»',
                   message=f'Привет {author_ann}! На Ваше объявление «{reply.announcement.announcement_preview()}» оставили новый отлик!',
                   recipient_list=[author_ann.email],
                   consolemessage=f'SysInfo: Отправлено письмо о принятии отлика для {author_ann}'
                   )
