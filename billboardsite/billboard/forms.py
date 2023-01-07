from django import forms

from billboard.models import Category, Announcement


class AnnouncementForm(forms.ModelForm):
    title = forms.CharField(min_length=4,
                            help_text='Введите заголовок объявления',
                            label='Заголовок')
    content = forms.CharField(min_length=4,
                              help_text='О чём Ваше объявление?',
                              widget=forms.Textarea,
                              label='Содержание')
    is_published = forms.BooleanField(required=False,
                                      label='Опубликовать')

    category = forms.ModelChoiceField(empty_label='Выберите категорию',
                                      queryset=Category.objects.all(),
                                      label='Категория')

    class Meta:
        model = Announcement
        fields = ['title', 'content', 'is_published', 'category']
