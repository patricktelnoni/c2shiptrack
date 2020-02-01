import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'c2shiptrack.settings')

app = Celery('project')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()