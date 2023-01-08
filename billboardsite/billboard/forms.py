from django import forms
from django.forms.widgets import CheckboxInput
from ckeditor_uploader.widgets import CKEditorUploadingWidget

from billboard.models import Category, Announcement


class AnnouncementForm(forms.ModelForm):
    title = forms.CharField(min_length=4,
                            label='Заголовок',
                            widget=forms.Textarea(attrs={'placeholder': 'Введите заголовок объявления',
                                                         'rows': '2',
                                                         'cols': '85%'
                                                         }))
    content = forms.CharField(min_length=4,
                              widget=CKEditorUploadingWidget(attrs={'placeholder': 'О чём Ваше объявление?',}),
                              label='Содержание')
    is_published = forms.BooleanField(required=False,
                                      widget=CheckboxInput,
                                      label='Опубликовать')

    category = forms.ModelChoiceField(empty_label='Выберите категорию',
                                      queryset=Category.objects.all(),
                                      label='Категория')

    class Meta:
        model = Announcement
        fields = ['title', 'content', 'is_published', 'category']
