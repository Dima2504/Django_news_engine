import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'news_engine.settings')

app = Celery('news_engine')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()