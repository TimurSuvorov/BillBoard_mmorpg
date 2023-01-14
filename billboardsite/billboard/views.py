from django.conf.global_settings import LOGIN_URL
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.core.mail import send_mail
from django.http import HttpResponseRedirect, HttpRequest
from django.urls import reverse_lazy, reverse
from django.views.generic.edit import FormMixin
from pprint import pprint
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from billboardsite.settings import DEFAULT_FROM_EMAIL
from .custom_mixins import OwnerOrAdminAnnouncePermissionCheck
from .filters import AnnouncementFilter, ReplyFilter, AnnouncementSearchFilter
from .forms import AnnouncementForm, ReplyForm
from .models import Announcement, Category, Reply
from .signals import reply_approved_signal
from .utils import check_perm_reply_action, check_perm_reply_add


class AnnouncementList(ListView):
    model = Announcement
    context_object_name = 'all_announcement'
    template_name = 'billboard/announcement_list.html'
    paginate_by = 6

    def get_queryset(self):
        self.queryset = Announcement.objects.filter(is_published=True).order_by('-time_update')
        self.filtered_queryset = AnnouncementFilter(data=self.request.GET,
                                                    queryset=self.queryset,
                                                    request=self.request)
        return self.filtered_queryset.qs

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['announcement_list_selected'] = 1
        context['filtered_queryset'] = self.filtered_queryset
        return context


class AnnouncementDetail(DetailView, FormMixin):
    model = Announcement
    form_class = ReplyForm
    context_object_name = 'announcement_detail'
    template_name = 'billboard/announcement_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['category_selected'] = self.object.category.id
        context['replies'] = self.object.replies.all()
        return context

    def post(self, request: HttpRequest, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseRedirect(LOGIN_URL)
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        announcement = Announcement.objects.get(pk=self.kwargs['pk'])
        check_perm_reply_add(self.request, announcement)  # Запрет на отклик к своим же постам
        form.instance = form.save(commit=False)
        form.instance.announcement = announcement
        form.instance.author_repl = self.request.user
        form.save()
        announcement.count_replies()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('announcement_detail', kwargs={'pk': self.kwargs['pk']})


class AnnouncementCreate(LoginRequiredMixin, CreateView):
    model = Announcement
    form_class = AnnouncementForm
    template_name = 'billboard/announcement_create.html'

    def form_valid(self, form):
        form.instance.author_ann = User.objects.get(username=self.request.user)
        return super().form_valid(form)


class AnnouncementUpdate(LoginRequiredMixin, UpdateView):
    model = Announcement
    raise_exception = True
    form_class = AnnouncementForm
    template_name = 'billboard/announcement_edit.html'

    def form_valid(self, form):
        announcement = self.get_object()
        if self.request.user != announcement.author_ann:
            raise PermissionDenied('not_author_of_ann')
        return super().form_valid(form)


class AnnouncementDelete(LoginRequiredMixin, OwnerOrAdminAnnouncePermissionCheck, DeleteView):
    permission_required = ''
    model = Announcement
    template_name = 'billboard/announcement_delete.html'
    success_url = reverse_lazy('announcement_list')


class AnnouncementSearch(ListView):
    model = Announcement
    context_object_name = 'all_announcement'
    template_name = 'billboard/announcement_search.html'
    paginate_by = 6

    def get_queryset(self):
        queryset_ann = Announcement.objects.filter(is_published=True).order_by('-time_update')
        queryset_auth = User.objects.filter(username__in=queryset_ann.values_list('author_ann__username', flat=True))
        self.filtered_queryset = AnnouncementSearchFilter(data=self.request.GET,
                                                          queryset=queryset_ann,
                                                          queryset_auth=queryset_auth)
        return self.filtered_queryset.qs

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['announcement_search_selected'] = 1
        context['filtered_queryset'] = self.filtered_queryset
        return context


class AnnWithReplyForMeList(LoginRequiredMixin, ListView):
    model = Announcement
    context_object_name = 'anns_with_reply_forme'
    template_name = 'billboard/reply_forme_list.html'
    paginate_by = 6

    def get_queryset(self):
        # Берем МОИ объявления, где есть отлики
        self.queryset_ann = Announcement.objects.filter(Q(author_ann__username=self.request.user) &
                                                    Q(num_replies__gt=0) &
                                                    Q(is_published__gt=0)
                                                    ).order_by('-time_update')
        # Вытаскиваем по ним категории
        cat_list = self.queryset_ann.values_list('category__id', flat=True)
        self.queryset_cat = Category.objects.filter(id__in=cat_list)
        # Применяем фильтр
        self.filtered_queryset = ReplyFilter(self.queryset_cat, self.request.GET, self.queryset_ann)
        return self.filtered_queryset.qs

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['reply_forme_list_selected'] = 1
        context['filtered_queryset'] = self.filtered_queryset
        return context


class ReplyMyList(LoginRequiredMixin, ListView):
    model = Announcement
    context_object_name = 'anns_with_reply_my'
    template_name = 'billboard/reply_my_list.html'
    paginate_by = 6

    def get_queryset(self):
        # Берем ВСЕ объявления и где есть МОИ отлики
        self.ann_with_reply_my = Reply.objects.filter(author_repl=self.request.user).values_list('announcement', flat=True)
        self.queryset_ann = Announcement.objects.filter(Q(is_published__gt=0) &
                                                        Q(pk__in=self.ann_with_reply_my)
                                                        ).order_by('-time_update')
        # Вытаскиваем по ним категории
        cat_list = self.queryset_ann.values_list('category__id', flat=True)
        self.queryset_cat = Category.objects.filter(id__in=cat_list)
        # Применяем фильтр
        self.filtered_queryset = ReplyFilter(self.queryset_cat, self.request.GET, self.queryset_ann)
        return self.filtered_queryset.qs

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['reply_my_list_selected'] = 1
        context['filtered_queryset'] = self.filtered_queryset
        return context


class ReplyDelete(LoginRequiredMixin, DeleteView):
    model = Reply
    template_name = 'billboard/reply_delete.html'

    def get_success_url(self):
        announcement = self.object.announcement
        return reverse('announcement_detail', kwargs={'pk': announcement.pk})

    def form_valid(self, form):
        # Сначало считываем информацию об удаляемой объекте, потом удаляем
        announcement = self.object.announcement
        success_url = self.get_success_url()
        self.object.delete()
        announcement.count_replies()
        return HttpResponseRedirect(success_url)


class CategoryListView(ListView):
    model = Announcement
    ordering = ['-time_update']
    template_name = 'billboard/announcement_by_category.html'
    context_object_name = 'category_announcement'

    def get_queryset(self):
        self.category = get_object_or_404(Category, pk=self.kwargs['pk'])
        queryset = Announcement.objects.filter(Q(category=self.category) & Q(is_published__gt=0)).order_by('-time_update').order_by('-time_create')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['category'] = self.category
        context['category_selected'] = self.kwargs['pk']
        return context


@login_required
def reply_approve(request, pk):
    reply = Reply.objects.get(pk=pk)
    check_perm_reply_action(request, reply)
    reply.is_approved = 'approved'
    reply.save()
    reply_approved_signal.send_robust(sender=Reply, instance=reply, path=request.META['HTTP_REFERER'])
    announcement_pk = reply.announcement.pk

    return HttpResponseRedirect(reverse('announcement_detail', kwargs={'pk': announcement_pk}))


@login_required
def reply_declain(request, pk):
    reply = Reply.objects.get(pk=pk)
    check_perm_reply_action(request, reply)
    reply.is_approved = 'declained'
    reply.save()
    announcement_pk = reply.announcement.pk
    return HttpResponseRedirect(reverse('announcement_detail', kwargs={'pk': announcement_pk}))


@login_required
def reply_reset(request, pk):
    reply = Reply.objects.get(pk=pk)
    check_perm_reply_action(request, reply)
    reply.is_approved = 'no_status'
    reply.save()
    announcement_pk = reply.announcement.pk
    return HttpResponseRedirect(reverse('announcement_detail', kwargs={'pk': announcement_pk}))