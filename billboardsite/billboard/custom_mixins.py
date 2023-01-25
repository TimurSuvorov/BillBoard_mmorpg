from django import forms
from django.shortcuts import get_object_or_404
from django.views.generic import View, DetailView
from django.forms.widgets import CheckboxInput
from ckeditor_uploader.widgets import CKEditorUploadingWidget

from .models import *
from django.core.exceptions import PermissionDenied


class CustomDetailView(DetailView):
    # For SQL-request optimization
    def get_object(self, queryset=None):
        object_ = get_object_or_404(self.model.objects.select_related('category'), pk=self.kwargs['pk'])
        return object_

    # For increase pageviews
    def get(self, request, *args, **kwargs):
        render_to_response = super().get(request, *args, **kwargs)
        self.object.pageviews_plus()
        return render_to_response


class OwnerOrAdminAnnounceCheckMixin(View):

    def form_valid(self, form):
        if (not self.request.user.is_superuser) and self.request.user != self.object.author_ann:
            raise PermissionDenied('not_author_of_ann')
        return super().form_valid(form)


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
