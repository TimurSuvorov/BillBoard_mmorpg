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


@register.inclusion_tag('billboard/tags_categories_block.html', takes_context=True, name='tag_categories_block')
def tag_categories_block(context):
    category_selected = context.get('category_selected', 0)
    categories = Category.objects.all()
    return {'categories': categories,
            'category_selected': category_selected}
