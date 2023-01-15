from django import forms
from django.forms.widgets import CheckboxInput
from ckeditor_uploader.widgets import CKEditorUploadingWidget

from .models import *
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.exceptions import PermissionDenied


class OwnerOrAdminAnnouncePermissionCheck(PermissionRequiredMixin):

    def has_permission(self):
        announcement = self.get_object()
        if (not self.request.user.is_superuser) and self.request.user != announcement.author_ann:
            raise PermissionDenied('not_author_of_ann')
        perms = self.get_permission_required()
        return self.request.user.has_perms(perms)


class CommonForm(forms.ModelForm):
    title = forms.CharField(min_length=4,
                            label='Заголовок',
                            widget=forms.Textarea(attrs={'placeholder': 'Какой будет заголовок?',
                                                         'rows': '2',
                                                         'cols': '85%'
                                                         }))
    content = forms.CharField(min_length=4,
                              widget=CKEditorUploadingWidget(attrs={'placeholder': 'Теперь введите более подробное описание...',}),
                              label='Содержание')
    is_published = forms.BooleanField(required=False,
                                      initial=True,
                                      widget=CheckboxInput,
                                      label='Опубликовать')

    category = forms.ModelChoiceField(empty_label='Выберите категорию...',
                                      queryset=Category.objects.all(),
                                      label='Категория')
