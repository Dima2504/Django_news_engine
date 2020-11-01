import os
from celery import Celery
from celery.schedules import crontab

from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'news_engine.settings')

app = Celery('news_engine')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    f'pick-news-every-{settings.NEWSAPI_TIMEDELTA_MINUTES}-minutes': {
        'task': 'news.tasks.pick_beat_news',
        'schedule': crontab(minute=f'*/{settings.NEWSAPI_TIMEDELTA_MINUTES}'),
    },
}