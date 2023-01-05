from django.shortcuts import render
from django.views.generic import ListView

from billboard.models import Announcement


# Create your views here.

def index(request):
    return render(request, 'billboard/base.html')


class AnnouncementList(ListView):
    model = Announcement
    ordering = '-time_update'
    context_object_name = 'all_announcement'
    template_name = 'billboard/announcement_list.html'


