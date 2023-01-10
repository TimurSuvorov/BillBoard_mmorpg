import re

from django import template

register = template.Library()

@register.filter()
def status_translate(status_value):
    status_dict = {'approved': 'Принят',
                   'declained': 'Отклонен',
                   'no_status': 'Без статуса'
    }

    return status_dict[status_value]
