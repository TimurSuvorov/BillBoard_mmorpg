from django.urls import path

from .views import index, AnnouncementList

urlpatterns = [
    path('', index),
    path('announcements/', AnnouncementList.as_view(), name='announcement_list' ),
]