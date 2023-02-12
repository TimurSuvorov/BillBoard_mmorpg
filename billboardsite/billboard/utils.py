import time

from io import BytesIO
from PIL import Image
from functools import wraps

from django.core.files import File
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


def check_resize_image(file, suffix_name, base_size: tuple = (150, 150)):
    with Image.open(file) as img:
        img_w, img_h = img.size
        # Обрезка-квадрат по минимальной стороне
        img_new = img.crop(((img_w - min(img.size)) // 2,
                            (img_h - min(img.size)) // 2,
                            (img_w + min(img.size)) // 2,
                            (img_h + min(img.size)) // 2))
        # Создание миниатюры
        img_new.thumbnail(base_size)
        img_new = img_new.convert('RGB')  # В случае RGBA изображения
        thumb_io = BytesIO()  # Создание BytesIO объекта
        img_new.save(thumb_io, format='JPEG', quality=95)  # Сохранение изображения в BytesIO объект
        new_name = f'photo_{suffix_name}_{time.time_ns()}.jpeg'
        new_image = File(thumb_io, name=new_name)  # Создание File объекта, который будет воспринимать поле ImageField модели
        return new_image


def disable_for_loaddata(signal_handler):
    """
    Decorator that turns off signal handlers when loading fixture data.
    """
    @wraps(signal_handler)
    def wrapper(*args, **kwargs):
        if kwargs.get('raw'):
            return
        signal_handler(*args, **kwargs)
    return wrapper
