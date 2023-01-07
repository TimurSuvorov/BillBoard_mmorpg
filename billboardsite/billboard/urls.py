from django.urls import path

from .views import index, AnnouncementList, AnnouncementListDetail, CategoryListView

urlpatterns = [
    path('', index),
    path('announcements/', AnnouncementList.as_view(), name='announcement_list'),
    path('announcements/<int:pk>', AnnouncementListDetail.as_view(), name='announcement_detail'),
    path('category/<int:pk>', CategoryListView.as_view(), name='announcement_by_category'),
]