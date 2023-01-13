import django_filters
from django import forms
from django.contrib.auth.models import User

from billboard.models import Announcement


def get_current_user(request):
    if request is None:
        return User.objects.none()
    user = request.user
    return User.objects.filter(username=user)


class AnnouncementFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(field_name='title',
                                      lookup_expr='icontains',
                                      widget=forms.TextInput(attrs={'type': 'search',
                                                                    'class': 'form-control',
                                                                    'placeholder': "Поиск по объявлениям..."}
                                                             )
                                      )

    author_ann = django_filters.ModelChoiceFilter(queryset=get_current_user,
                                                  field_name='author_ann',
                                                  widget=forms.RadioSelect(attrs={'onChange': 'this.form.submit()',
                                                                                  'label.text': ''})
                                                 )


    class Meta:
        model = Announcement
        fields = ['title', 'author_ann']


class ReplyFilter(django_filters.FilterSet):
    def __init__(self, queryset_cat, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.filters['title'].queryset = self.queryset
        self.filters['category'].queryset = queryset_cat

    title = django_filters.ModelMultipleChoiceFilter(queryset=None,
                                                     field_name='title',
                                                     lookup_expr='icontains',
                                                     label='Обьявление',
                                                     )


    category = django_filters.ModelMultipleChoiceFilter(queryset=None,
                                                        field_name='category__catname',
                                                        widget=forms.CheckboxSelectMultiple(),
                                                        label='Категория',
                                                        )



