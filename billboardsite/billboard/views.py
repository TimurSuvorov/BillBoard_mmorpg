from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.urls import reverse_lazy, reverse
from django.views.generic.edit import FormMixin
from pprint import pprint

from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib import messages

from billboard.custom_mixins import OwnerOrAdminAnnouncePermissionCheck
from billboard.forms import AnnouncementForm, ReplyForm
from billboard.models import Announcement, Category, Reply


# Create your views here.

def index(request):
    return render(request, 'billboard/index.html')


class AnnouncementList(ListView):
    model = Announcement
    context_object_name = 'all_announcement'
    template_name = 'billboard/announcement_list.html'
    paginate_by = 6

    def get_queryset(self):
        queryset = Announcement.objects.filter(is_published=True).order_by('-time_create', '-time_update')
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['list_selected'] = 1
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

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        announcement = Announcement.objects.get(pk=self.kwargs['pk'])
        # Запрет на отклик к своим же постам
        if self.request.user == announcement.author_ann:
            raise PermissionDenied('reply_for_yourself')

        self.myform = form.save(commit=False)
        self.myform.announcement = announcement
        self.myform.author_repl = self.request.user
        self.myform.announcement.count_replies()
        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('announcement_detail', kwargs={'pk': self.kwargs['pk']})


class AnnouncementCreate(CreateView):
    model = Announcement
    form_class = AnnouncementForm
    template_name = 'billboard/announcement_create.html'

    def form_valid(self, form):
        form.instance.author_ann = User.objects.get(username=self.request.user)
        return super().form_valid(form)


class AnnouncementUpdate(UpdateView):
    model = Announcement
    raise_exception = True
    form_class = AnnouncementForm
    template_name = 'billboard/announcement_edit.html'

    def form_valid(self, form):
        announcement = self.get_object()
        if self.request.user != announcement.author_ann:
            raise PermissionDenied('not_author_of_ann')
        return super().form_valid(form)


class AnnouncementDelete(DeleteView):
    model = Announcement
    template_name = 'billboard/announcement_delete.html'
    success_url = reverse_lazy('announcement_list')


class ReplyDelete(DeleteView):
    model = Reply
    template_name = 'billboard/reply_delete.html'

    def get_success_url(self):
        announcement = self.object.announcement
        print(announcement)
        return reverse('announcement_detail', kwargs={'pk': announcement.pk})

# class ReplyCreate(CreateView):
#     model = Reply
#     form_class = ReplyForm
#     template_name = 'billboard/reply_create.html'
#
#     def form_valid(self, form):
#         form.instance.author_repl = User.objects.get(username=self.request.user)
#         form.save.announcement =
#         return super().form_valid(form)


class CategoryListView(ListView):
    model = Announcement
    ordering = ['-time_update']
    template_name = 'billboard/announcement_by_category.html'
    context_object_name = 'category_announcement'

    def get_queryset(self):
        self.category = get_object_or_404(Category, pk=self.kwargs['pk'])
        queryset = Announcement.objects.filter(category=self.category).order_by('-time_update').order_by('-time_create')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['category'] = self.category
        context['category_selected'] = self.kwargs['pk']
        return context
