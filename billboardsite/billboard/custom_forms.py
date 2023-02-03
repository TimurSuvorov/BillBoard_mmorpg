from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms
from django.core.exceptions import ValidationError
from django.db.models.fields.files import ImageFieldFile
from django.forms import CheckboxInput

from billboard.models import Category
from billboard.utils import check_resize_image
from billboardsite.settings import IMAGE_ALLOWED_FORMATS, IMAGE_MIN_SIZE


class CommonForm(forms.ModelForm):

    allowed_formats_ = ', '.join(IMAGE_ALLOWED_FORMATS).replace('image/', '.')
    min_size_ = '*'.join(map(str, IMAGE_MIN_SIZE))

    title = forms.CharField(min_length=4,
                            label='Заголовок',
                            widget=forms.Textarea(attrs={'placeholder': 'Какой будет заголовок?',
                                                         'rows': '1',
                                                         'cols': '85%'
                                                         }))
    content = forms.CharField(min_length=4,
                              widget=CKEditorUploadingWidget(attrs={'placeholder': 'Теперь введите более подробное описание...',}),
                              label='Содержание')
    photoimage = forms.ImageField(label='Миниатюра',
                                  help_text='Поддерживаемые форматы: {allowed_formats}. \n'
                                            'Минимальное разрешение: {min_size}.'.format(allowed_formats=allowed_formats_, min_size=min_size_),
                                  error_messages={'invalid_image': 'Загрузите изображение повторно. '
                                                  'Загруженный вами файл либо не был изображением, либо был поврежден.'},
                                  required=False,
                                  )
    is_published = forms.BooleanField(required=False,
                                      initial=True,
                                      widget=CheckboxInput,
                                      label='Опубликовать')

    category = forms.ModelChoiceField(empty_label='Выберите категорию...',
                                      queryset=Category.objects.all(),
                                      label='Категория')

    def clean_photoimage(self):
        upl_photo = self.cleaned_data['photoimage']
        # Если поле в POST пустое, то при создании None, при редактировании - ImageFieldFile
        if upl_photo and not isinstance(upl_photo, ImageFieldFile):
            if upl_photo.content_type in IMAGE_ALLOWED_FORMATS and \
                    (upl_photo.image.size[0] >= 150 and upl_photo.image.size[1] >= 150):
                upl_photo_ = check_resize_image(upl_photo,
                                                f'{self.instance.__class__.__name__}',
                                                IMAGE_MIN_SIZE
                                                )
                return upl_photo_
            raise ValidationError(message='Ошибка загрузки: Неверный формат изображения или маленькое разрешение')
