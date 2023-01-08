from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from pprint import pprint

from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib import messages

from billboard.custom_mixins import OwnerOrAdminAnnouncePermissionCheck
from billboard.forms import AnnouncementForm
from billboard.models import Announcement, Category


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


class AnnouncementDetail(DetailView):
    model = Announcement
    context_object_name = 'announcement_detail'
    template_name = 'billboard/announcement_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['category_selected'] = self.object.category.id
        return context


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
