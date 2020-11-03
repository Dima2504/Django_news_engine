import os
from celery import Celery
from celery.schedules import crontab

from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'news_engine.settings')

app = Celery('news_engine')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    f'pick-news-every-{settings.NEWS_API_REQUEST_TIMEDELTA_MINUTES}-minutes': {
        'task': 'news.tasks.pick_beat_news',
        'schedule': crontab(minute=f'*/{settings.NEWS_API_REQUEST_TIMEDELTA_MINUTES}'),
    },
    f'clear-db-every-{settings.NEWS_CLEAR_DB_TIMEDELTA_DAYS}-days': {
        'task': 'news.task.clear_db',
        'schedule': crontab(minute=0, hour=f'*/{24*settings.NEWS_CLEAR_DB_TIMEDELTA_DAYS}'),
    },
}