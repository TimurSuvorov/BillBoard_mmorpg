import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'billboardsite.settings')

app = Celery('billboards')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()
