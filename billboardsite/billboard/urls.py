from django.urls import path

from .views import index, AnnouncementList, AnnouncementDetail, AnnouncementCreate, AnnouncementUpdate, AnnouncementDelete, CategoryListView

urlpatterns = [
    path('', index),
    path('announcements/', AnnouncementList.as_view(), name='announcement_list'),
    path('announcements/<int:pk>', AnnouncementDetail.as_view(), name='announcement_detail'),
    path('announcements/create', AnnouncementCreate.as_view(), name='announcement_create'),
    path('announcements/<int:pk>/edit', AnnouncementUpdate.as_view(), name='announcement_edit'),
    path('announcements/<int:pk>/delete', AnnouncementDelete.as_view(), name='announcement_delete'),
    path('category/<int:pk>', CategoryListView.as_view(), name='announcement_by_category'),
]


