from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.exceptions import PermissionDenied


class OwnerOrAdminAnnouncePermissionCheck(PermissionRequiredMixin):

    def has_permission(self):
        announcement = self.get_object()
        if not self.request.user.is_superuser and self.request.user != announcement.author_ann:
            raise PermissionDenied('Вы не являетесь автором этой записи')
        perms = self.get_permission_required()
        return self.request.user.has_perms(perms)


