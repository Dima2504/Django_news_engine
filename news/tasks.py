from news_engine import celery_app

from .service import pick_top_headlines
from .service import delete_old_news_from_db
from .service import send_one_news_to_one_user

from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)


@celery_app.task
def pick_beat_news():
    pick_top_headlines()
    logger.info('Got news from newsapi.org')


@celery_app.task
def clear_db():
    logger.info('Before deleting')
    delete_old_news_from_db()


@celery_app.task
def send_one_news_to_one_user_task(user_id):
    send_one_news_to_one_user(user_id)
