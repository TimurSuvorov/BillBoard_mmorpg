from django.core.files.uploadedfile import InMemoryUploadedFile
from io import BytesIO

from django import forms
from django.core.exceptions import ValidationError

from .custom_mixins import CommonForm
from .models import Announcement, Reply, Newsletter, UserProfile
from .utils import check_resize_image

IMAGE_ALLOWED_FORMATS = ['image/jpeg', 'image/jpg', 'image/png']
IMAGE_MIN_SIZE = (150, 150)


class AnnouncementForm(CommonForm):

    class Meta:
        model = Announcement
        fields = ['title', 'content', 'is_published', 'category']


class NewsLetterForm(CommonForm):

    class Meta:
        model = Newsletter
        fields = ['title', 'content', 'is_published', 'category']


class ReplyForm(forms.ModelForm):
    content = forms.CharField(min_length=4,
                              label='Текст отлика',
                              widget=forms.Textarea(attrs={'placeholder': 'Введите текст отклика',
                                                           'rows': '4',
                                                           'cols': '85%'
                                                           }
                                                    )
                              )

    class Meta:
        model = Reply
        fields = ['content']


class UserProfileForm(forms.ModelForm):

    allowed_formats_ = ', '.join(IMAGE_ALLOWED_FORMATS).replace('image/', '.')
    min_size_ = '*'.join(map(str, IMAGE_MIN_SIZE))

    photoprofile = forms.ImageField(help_text='Поддерживаемые форматы: {allowed_formats}. \n'
                                              'Минимальное разрешение: {min_size}.'.format(allowed_formats=allowed_formats_, min_size=min_size_),
                                    error_messages={'invalid_image': 'Загрузите изображение повторно. '
                                                    'Загруженный вами файл либо не был изображением, либо был поврежден.'},
                                    )



    class Meta:
        model = UserProfile
        fields = ['nickname', 'photoprofile', 'aboutme', 'timezone', 'is_replies_alerts', 'appr_replies_alerts', 'is_news_subscribe']
        widgets = {
            'aboutme': forms.Textarea(attrs={'placeholder': 'Немного о себе...',
                                             'rows': '2',
                                             'cols': '85%'
                                             }),
        },
        labels = {
            'nickname': 'Никнейм:',
            'aboutme': 'Немного о себе:',
            'timezone': 'Часовой пояс:',
        }

    def clean_photoprofile(self):
        upl_photo = self.cleaned_data['photoprofile']
        if isinstance(upl_photo, InMemoryUploadedFile):  # Если поле в POST пустое, то ImageFieldFile
            if upl_photo.content_type in IMAGE_ALLOWED_FORMATS and \
                    (upl_photo.image.size[0] >= 150 and upl_photo.image.size[1] >= 150):
                upl_photo_ = check_resize_image(upl_photo, self.instance.user, IMAGE_MIN_SIZE)
                return upl_photo_
            raise ValidationError(message='Ошибка загрузки: Неверный формат изображения или маленькое разрешение')


