import django_filters
from django import forms
from django.contrib.auth.models import User
from django.forms import DateInput

from billboard.models import Announcement


class AnnouncementFilter(django_filters.FilterSet):

    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request

    title = django_filters.CharFilter(field_name='title',
                                      lookup_expr='icontains',
                                      widget=forms.TextInput(attrs={'type': 'search',
                                                                    'class': 'form-control',
                                                                    'placeholder': "Поиск по объявлениям..."}
                                                             )
                                      )

    is_author_ann = django_filters.BooleanFilter(field_name='author_ann',
                                                 method='ann_by_author',
                                                 widget=forms.CheckboxInput(attrs={'onChange': 'this.form.submit()'})
                                                 )

    def ann_by_author(self, queryset, name, value):
        if value:  # Значение True или False из CheckboxInput()
            return queryset.filter(author_ann__username=self.request.user)
        return queryset

    class Meta:
        model = Announcement
        fields = ['title']


class ReplyFilter(django_filters.FilterSet):
    def __init__(self, queryset_cat, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.filters['title'].queryset = self.queryset
        self.filters['category'].queryset = queryset_cat

    title = django_filters.ModelMultipleChoiceFilter(queryset=None,
                                                     field_name='title',
                                                     lookup_expr='icontains',
                                                     label='Обяявление',
                                                     )

    category = django_filters.ModelMultipleChoiceFilter(queryset=None,
                                                        field_name='category__catname',
                                                        widget=forms.CheckboxSelectMultiple(),
                                                        label='Категория',
                                                        )

    class Meta:
        model = Announcement
        fields = ['title', 'category']

class AnnouncementSearchFilter(django_filters.FilterSet):

    def __init__(self, queryset_auth, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.filters['author_ann'].queryset = queryset_auth

    title = django_filters.CharFilter(field_name='title',
                                      lookup_expr='icontains',
                                      label='Заголовок',
                                      widget=forms.TextInput(attrs={'type': 'search',
                                                                    'placeholder': 'Поиск в заголовке...',
                                                                    })
                                      )

    content = django_filters.CharFilter(field_name='content',
                                        lookup_expr='icontains',
                                        label='Содержание',
                                        widget=forms.TextInput(attrs={'type': 'search',
                                                                      'placeholder': 'Поиск в содержании...',
                                                                      })
                                        )

    time_create = django_filters.DateFilter(field_name='time_create',
                                            lookup_expr='gt',
                                            label='Время публикации',
                                            widget=DateInput(format='%d/%m/%Y',
                                                             attrs={'type': 'date',
                                                                    'placeholder': 'Создано, начиная с...',
                                                                    },

                                                             ),
                                            )

    time_update = django_filters.DateFilter(field_name='time_create',
                                            lookup_expr='gt',
                                            label='Время обновления',
                                            widget=DateInput(format='%d/%m/%Y',
                                                             attrs={'type': 'date',
                                                                    'placeholder': 'Обновлено, начиная с...'},
                                                             ),
                                            )

    author_ann = django_filters.ModelMultipleChoiceFilter(queryset=None,
                                                          field_name='author_ann',
                                                          widget=forms.CheckboxSelectMultiple(),
                                                          label='Авторы объявлений',
                                                          )


    class Meta:
        model = Announcement
        fields = ['title', 'content', 'time_create', 'time_update', 'author_ann']