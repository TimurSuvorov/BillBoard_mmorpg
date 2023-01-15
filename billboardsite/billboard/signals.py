from allauth.account.models import EmailAddress
from django.contrib.auth.models import Group
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver, Signal

from billboardsite import settings
from .models import *
from .utils import sendsimplemail

# Отдельный сигнал для передачи доп.аргументов
reply_approved_signal = Signal()


# Сигнал нового пользователя(прохождение верификации)
@receiver(post_save, sender=EmailAddress)
def new_user_actions(sender, instance, **kwargs):
    if instance.verified:  # Когда проведена верификация по email
        sendsimplemail(subject=f'Привет {instance.user}!',
                       message=f'Привет {instance.user}! Добро пожаловать на наш сайт «MMORPG Billboard»',
                       recipient_list=[instance.email],
                       consolemessage=f'SysInfo: Отправлено письмо новому пользователю {instance.user}'
                       )

        # Добавление пользователя в группу 'common_users'
        common_group = Group.objects.get(name='common_users')
        common_group.user_set.add(instance.user)


@receiver(reply_approved_signal, sender=Reply)
def reply_approved(sender, instance, **kwargs):
    if instance.is_approved == 'approved':
        author_ann = instance.announcement.author_ann
        sendsimplemail(subject=f'Отклик принят: «{instance.reply_preview()}»',
                       message=f'Привет {instance.author_repl}! Ваш отклик «{instance.reply_preview()}» принят пользователем {author_ann}!'
                               f'\nСсылка на Ваше объявление: {kwargs["path"]}',
                       recipient_list=[instance.author_repl.email],
                       consolemessage=f'SysInfo: Отправлено письмо о принятии отлика для {instance.author_repl}'
                       )


@receiver(post_save, sender=Newsletter)
def newsletter_sent(sender, instance, **kwargs):
    if instance.is_published and not instance.is_sent:
        all_users = User.objects.all()
        for user in all_users:
            sendsimplemail(subject=f'Новость от «MMORPG Billboard» «{instance.newsletter_preview()}»',
                           message=f'Привет {user.username}! Вышла новость «{instance.newsletter_preview()}» от наших экспертов «MMORPG Billboard»!',
                           recipient_list=[user.email],
                           consolemessage=f'SysInfo: Отправлено письмо о новости для {user.username}'
                           )
