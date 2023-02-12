from allauth.account.models import EmailAddress
from django.db.models.signals import post_save
from django.dispatch import receiver

from .tasks import *
from .utils import disable_for_loaddata


# Сигнал нового пользователя(прохождение верификации)
@receiver(post_save, sender=EmailAddress)
@disable_for_loaddata
def new_user_actions(sender, instance, **kwargs):
    if instance.verified:
        new_user_actions_async.delay(user_id=instance.user_id)


@receiver(post_save, sender=User)
@disable_for_loaddata
def super_user_processing(sender, instance, created, **kwargs):
    if created and instance.is_superuser:
        # Добавление суперпользователя в группы
        all_group = Group.objects.all()
        for group in all_group:
            group.user_set.add(instance)

        # Добавление профиля по умолчанию
        UserProfile.objects.get_or_create(user=instance, nickname=instance.username)


@receiver(post_save, sender=Reply)
@disable_for_loaddata
def reply_change_mail(sender, instance, **kwargs):
    if kwargs['created']:
        new_reply_mail_async.delay(pk=instance.pk)
    elif instance.is_approved == 'approved':
        reply_approved_mail_async.delay(pk=instance.pk)


@receiver(post_save, sender=Newsletter)
@disable_for_loaddata
def newsletter_mail(sender, instance, **kwargs):
    if instance.is_published and not instance.is_sent:
        newsletter_mail_async.delay(pk=instance.pk)


