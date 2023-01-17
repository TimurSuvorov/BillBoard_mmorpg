from django import forms
from django.forms.widgets import CheckboxInput
from ckeditor_uploader.widgets import CKEditorUploadingWidget

from billboard.custom_mixins import CommonForm
from billboard.models import Category, Announcement, Reply, Newsletter, UserProfile


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

    class Meta:
        model = UserProfile
        fields = ['nickname', 'aboutme', 'timezone', 'is_replies_alerts', 'is_news_subscribe']