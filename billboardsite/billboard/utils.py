from django.core.exceptions import PermissionDenied
from django.core.mail import send_mail

from billboardsite import settings


def check_perm_reply_action(request, reply_object):
    if request.user == reply_object.author_repl:
        raise PermissionDenied('action_with_yourself_reply')
    if request.user != reply_object.announcement.author_ann:
        raise PermissionDenied('not_author_of_ann')


def check_perm_reply_add(request, ann_object):
    if request.user == ann_object.author_ann:
        raise PermissionDenied('reply_for_yourself_ann')


def sendsimplemail(subject, message, recipient_list, consolemessage=None):
    send_mail(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=recipient_list
    )
    if consolemessage:
        print(f'Mail send: {consolemessage}')
