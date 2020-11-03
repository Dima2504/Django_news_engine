from news_engine import celery_app

from .service import pick_top_headlines
from .service import delete_old_news_from_db


@celery_app.task
def pick_beat_news():
    pick_top_headlines()


@celery_app.task
def clear_db():
    delete_old_news_from_db()