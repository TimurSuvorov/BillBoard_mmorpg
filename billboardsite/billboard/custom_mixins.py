from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView

from django.core.exceptions import PermissionDenied


class CustomDetailView(DetailView):
    # For SQL-request optimization
    def get_object(self, queryset=None):
        object_ = get_object_or_404(self.model.objects.select_related('category'), pk=self.kwargs['pk'])
        return object_

    # Increase pageviews
    def get(self, request, *args, **kwargs):
        render_to_response = super().get(request, *args, **kwargs)
        self.object.pageviews_plus()
        return render_to_response


class OwnerOrAdminAnnounceCheckMixin(PermissionRequiredMixin):

    def has_permission(self):
        if (not self.request.user.is_superuser) and self.request.user != self.get_object().author_ann:
            raise PermissionDenied('not_author_of_ann')
        perms = self.get_permission_required()
        return self.request.user.has_perms(perms)


class OwnerOrAdminReplyCheckMixin(PermissionRequiredMixin):

    def has_permission(self):
        if (not self.request.user.is_superuser) and self.request.user != self.get_object().author_repl:
            raise PermissionDenied('not_author_of_repl')
        perms = self.get_permission_required()
        return self.request.user.has_perms(perms)


class OwnerUserProfileCheckMixin(PermissionRequiredMixin):

    def has_permission(self):
        if self.request.user != self.get_object().user:
            raise PermissionDenied()
        perms = self.get_permission_required()
        return self.request.user.has_perms(perms)
