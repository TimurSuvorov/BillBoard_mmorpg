import datetime

from django import template
from billboard.models import Announcement, Category

register = template.Library()


@register.simple_tag()
def isupdated(pk):
    announcement = Announcement.objects.get(pk=pk)
    delta: datetime.timedelta = announcement.time_update - announcement.time_create
    if delta.seconds >= 60:
        return True
    return False

@register.simple_tag()
def get_categories():
    categories = Category.objects.all()
    return categories
