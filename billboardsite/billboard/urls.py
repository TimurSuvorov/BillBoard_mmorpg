from django.urls import path

from .views import *

urlpatterns = [
    path('announcements/', AnnouncementList.as_view(), name='announcement_list'),
    path('announcements/<int:pk>', AnnouncementDetail.as_view(), name='announcement_detail'),
    path('announcements/create', AnnouncementCreate.as_view(), name='announcement_create'),
    path('announcements/<int:pk>/edit', AnnouncementUpdate.as_view(), name='announcement_edit'),
    path('announcements/<int:pk>/delete', AnnouncementDelete.as_view(), name='announcement_delete'),
    path("announcements/search", AnnouncementSearch.as_view(), name="announcement_search"),

    path('category/<int:pk>', CategoryListView.as_view(), name='announcement_by_category'),

    path('replies/<int:pk>/approve', reply_approve, name='reply_approve'),
    path('replies/<int:pk>/declain', reply_declain, name='reply_declain'),
    path('replies/<int:pk>/reset', reply_reset, name='reply_reset'),
    path('replies/my', ReplyMyList.as_view(), name='reply_my_list'),
    path('replies/forme', AnnWithReplyForMeList.as_view(), name='reply_forme_list'),
    path('replies/<int:pk>/delete', ReplyDelete.as_view(), name='reply_delete'),

    path('newsletters/', NewsLetterList.as_view(), name='newsletter_list'),
    path('newsletters/<int:pk>', NewsLetterDetail.as_view(), name='newsletter_detail'),
    path('newsletters/create', NewsLetterCreate.as_view(), name='newsletter_create'),
    path('newsletters/<int:pk>/edit', NewsLetterUpdate.as_view(), name='newsletter_edit'),
    path('newsletters/<int:pk>/delete', NewsLetterDelete.as_view(), name='newsletter_delete'),
    path('newsletters/reqtonewsauthors', request_to_newsauthors, name='request_to_newsauthors'),
    path('newsletters/addtonewsauthors/<int:user_id>', add_to_newsauthors, name='add_to_newsauthors'),
    path('newsletters/declaintonewsauthors/<int:user_id>', declain_to_newsauthors, name='declain_to_newsauthors'),

    path('userprofile/<int:pk>/edit', UserProfileUpdate.as_view(), name='userprofile_edit'),

    path('customconfirmation/', confirmationproccessing, name='confirmationproccessing')
]


