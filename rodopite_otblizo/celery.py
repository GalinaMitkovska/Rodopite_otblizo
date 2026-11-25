import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rodopite_otblizo.settings')

app = Celery('rodopite_otblizo')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()