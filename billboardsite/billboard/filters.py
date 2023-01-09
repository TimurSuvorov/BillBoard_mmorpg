import django_filters
from django import forms

from billboard.models import Announcement


class AnnouncementFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(field_name='title',
                                      lookup_expr='icontains',
                                      widget=forms.TextInput(attrs={'type': 'search',
                                                                    'class': 'form-control',
                                                                    'placeholder': "Поиск по объявлениям..."}
                                                             )
                                      )
