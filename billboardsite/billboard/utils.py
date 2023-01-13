from django.core.exceptions import PermissionDenied


def check_perm_reply_action(request, reply_object):
    if request.user == reply_object.author_repl:
        raise PermissionDenied('action_with_yourself_reply')
    if request.user != reply_object.announcement.author_ann:
        raise PermissionDenied('not_author_of_ann')


def check_perm_reply_add(request, ann_object):
    if request.user == ann_object.author_ann:
        raise PermissionDenied('reply_for_yourself_ann')