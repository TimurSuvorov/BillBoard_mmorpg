import django_filters
from django import forms
from django.db.models import Q

from billboard.models import Announcement, Category


class AnnouncementFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(field_name='title',
                                      lookup_expr='icontains',
                                      widget=forms.TextInput(attrs={'type': 'search',
                                                                    'class': 'form-control',
                                                                    'placeholder': "Поиск по объявлениям..."}
                                                             )
                                      )

class ReplyFilter(django_filters.FilterSet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.filters['title'].queryset = self.queryset

    title = django_filters.ModelMultipleChoiceFilter(queryset=None,
                                                     field_name='title',
                                                     lookup_expr='icontains',
                                                     # widget=forms.MultipleChoiceField(attrs={})
                                                     )



    category = django_filters.ModelMultipleChoiceFilter(queryset=Category.objects.all(),
                                                        field_name='category__catname',
                                                        widget=forms.CheckboxSelectMultiple(attrs={'checked': 'checked'})
                                                        )



