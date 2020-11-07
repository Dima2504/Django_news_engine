from news_engine import celery_app

from .service import pick_top_headlines
from .service import delete_old_news_from_db
from .service import get_users_needed_news_contained_into_signatures


from news.models import History
from celery import chain
from celery import group
from django.core.mail import send_mail
from django.conf import settings
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
def send_one_news_to_user(subject, message, news_id, user_id, user_email):
    send_mail(subject, message, from_email=settings.DEFAULT_FROM_EMAIL, recipient_list=[user_email,])
    logger.info(f'User {user_id} receive news {news_id} on email')
    History.objects.create(user_id=user_id, news_id=news_id, is_checked_on_site=False, is_checked_on_email=True)
    logger.info(f'Create relationship with user {user_id} and news {news_id}')


@celery_app.task(bind=True)
def send(self):
    logger.info(f'starting task send: [{self.name}]')
    tasks = get_users_needed_news_contained_into_signatures(send_one_news_to_user)
    logger.info(f'get all users needed news')
    group([chain(*t) for t in tasks.values()]).apply_async()
