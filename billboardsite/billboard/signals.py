from allauth.account.models import EmailAddress
from django.contrib.auth.models import Group
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver, Signal

from billboardsite import settings
from .models import *

reply_approved_signal = Signal()


# Сигнал нового пользователя(прохождение верификации)
@receiver(post_save, sender=EmailAddress)
def new_user_signal(sender, instance, **kwargs):
    if instance.verified:  # Когда проведена верификация по email
        send_mail(
            subject=f'Привет {instance.user}!',
            message=f'Привет {instance.user}! Добро пожаловать на наш сайт MMORPG Billboard',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[instance.email]
        )

        # Добавление пользователя в группу 'common_users'
        common_group = Group.objects.get(name='common_users')
        common_group.user_set.add(instance.user)

        print(f'SysInfo: Отправлено письмо новому пользователю {instance.user}')



@receiver(reply_approved_signal, sender=Reply)
def reply_approved(sender, instance, **kwargs):
    if instance.is_approved == 'approved':
        author_ann = instance.announcement.author_ann
        send_mail(
            subject=f'Отклик принят: «{instance.reply_preview()}»',
            message=f'Привет {instance.author_repl}! Ваш отклик «{instance.reply_preview()}» принят пользователем {author_ann}!'
                    f'\nСсылка на Ваше объявление {kwargs["path"]}',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[instance.author_repl.email]
        )
        print(f'SysInfo: Отправлено письмо о принятии отлика для {instance.author_repl}')