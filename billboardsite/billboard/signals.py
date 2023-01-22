from allauth.account.models import EmailAddress
from django.db.models.signals import post_save
from django.dispatch import receiver

from .tasks import *


# Сигнал нового пользователя(прохождение верификации)
@receiver(post_save, sender=EmailAddress)
def new_user_actions(sender, instance, **kwargs):
    if instance.verified:
        new_user_actions_async.delay(user_id=instance.user_id)


@receiver(post_save, sender=Reply)
def reply_change_mail(sender, instance, **kwargs):
    if kwargs['created']:
        new_reply_mail_async.delay(pk=instance.pk)
    elif instance.is_approved == 'approved':
        reply_approved_mail_async.delay(pk=instance.pk)


@receiver(post_save, sender=Newsletter)
def newsletter_mail(sender, instance, **kwargs):
    if instance.is_published and not instance.is_sent:
        newsletter_mail_async.delay(pk=instance.pk)


