from allauth.account.models import EmailAddress
from django.contrib.auth.models import Group
from django.db.models.signals import post_save
from django.dispatch import receiver, Signal

from .models import *
from .utils import sendsimplemail
from .tasks import newsletter_mail_async, reply_approved_mail_async, new_user_actions_async

# Отдельный сигнал для передачи доп.аргументов
reply_approved_signal = Signal()


# Сигнал нового пользователя(прохождение верификации)
@receiver(post_save, sender=EmailAddress)
def new_user_actions(sender, instance, **kwargs):
    if instance.verified:  # Когда проведена верификация по email
        print(instance.user_id)
        new_user_actions_async.delay(instance.user_id)


@receiver(reply_approved_signal, sender=Reply)
def reply_approved_mail(sender, instance, **kwargs):
    if instance.is_approved == 'approved':
        reply_approved_mail_async.delay(pk=instance.pk, path=kwargs["path"])


@receiver(post_save, sender=Newsletter)
def newsletter_mail(sender, instance, **kwargs):
    if instance.is_published and not instance.is_sent:
        newsletter_mail_async.delay(instance.pk)


