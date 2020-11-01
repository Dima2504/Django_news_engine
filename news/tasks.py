from news_engine import celery_app

from .service import pick_top_headlines


@celery_app.task
def pick_beat_news():
    pick_top_headlines()