from allauth.account.models import EmailAddress
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import *
from .tasks import newsletter_mail_async, reply_approved_mail_async, new_user_actions_async, new_reply_mail_mail_async


# Сигнал нового пользователя(прохождение верификации)
@receiver(post_save, sender=EmailAddress)
def new_user_actions(sender, instance, **kwargs):
    if instance.verified:  # Когда проведена верификация по email
        new_user_actions_async.delay(user_id=instance.user_id)


@receiver(post_save, sender=Reply)
def new_reply_mail(sender, instance, **kwargs):
    if kwargs['created']:
        new_reply_mail_mail_async.delay(pk=instance.pk)


@receiver(post_save, sender=Reply)
def reply_approved_mail(sender, instance, **kwargs):
    if instance.is_approved == 'approved':
        reply_approved_mail_async.delay(pk=instance.pk)


@receiver(post_save, sender=Newsletter)
def newsletter_mail(sender, instance, **kwargs):
    if instance.is_published and not instance.is_sent:
        newsletter_mail_async.delay(pk=instance.pk)


