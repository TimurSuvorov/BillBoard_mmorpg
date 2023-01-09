from django.urls import path

from .views import *

urlpatterns = [
    path('', index),
    path('announcements/', AnnouncementList.as_view(), name='announcement_list'),
    path('announcements/<int:pk>', AnnouncementDetail.as_view(), name='announcement_detail'),
    path('announcements/create', AnnouncementCreate.as_view(), name='announcement_create'),
    path('announcements/<int:pk>/edit', AnnouncementUpdate.as_view(), name='announcement_edit'),
    path('announcements/<int:pk>/delete', AnnouncementDelete.as_view(), name='announcement_delete'),
    path('category/<int:pk>', CategoryListView.as_view(), name='announcement_by_category'),
    path('replies/<int:pk>/delete', ReplyDelete.as_view(), name='reply_delete'),
    path('replies/<int:pk>/approve', reply_approve, name='reply_approve'),
    path('replies/<int:pk>/declain', reply_declain, name='reply_declain'),
    path('replies/<int:pk>/reset', reply_reset, name='reply_reset'),
]


