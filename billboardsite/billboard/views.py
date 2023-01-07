from pprint import pprint

from django.shortcuts import render
from django.views.generic import ListView, DetailView

from billboard.models import Announcement, Category


# Create your views here.

def index(request):
    return render(request, 'billboard/index.html')


class AnnouncementList(ListView):
    model = Announcement
    ordering = '-time_update, -time_create'
    context_object_name = 'all_announcement'
    template_name = 'billboard/announcement_list.html'
    paginate_by = 3

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(AnnouncementList, self).get_context_data()
        pprint(context)
        return context

class AnnouncementListDetail(DetailView):
    model = Announcement
    context_object_name = 'announcement'
    template_name = 'billboard/announcement_detail.html'


class CategoryListView(ListView):
    model = Announcement
    ordering = '-time_update, -time_create'
    template_name = 'billboard/announcement_by_category.html'
    context_object_name = 'category_announcement'

    def get_queryset(self):
        self.category = Category.objects.get(pk=self.kwargs['pk'])
        queryset = Announcement.objects.filter(category=self.category).order_by('-time_update').order_by('-time_create')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['category'] = self.category
        context['cat_selected'] = self.kwargs['pk']
        return context
