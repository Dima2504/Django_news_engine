from news_engine import celery_app

from django.conf import settings
from django.core.mail import send_mail

from .service import pick_top_headlines
from .service import delete_old_news_from_db
from .service import send_one_news_to_one_user
from .service import send_one_news_on_telegram

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


@celery_app.task
def send_one_news_on_telegram_task(user_id):
    send_one_news_on_telegram(user_id)


@celery_app.task(bind=True)
def send_mail_task(self, user_email):
    if send_mail('Відгук на сайті Picle', 'Ваш відгук успішно прийнято, дякуємо, що користуєтеся сервісом. З повагою, адміністрація сайту :)', from_email=settings.DEFAULT_FROM_EMAIL, recipient_list=[user_email, ]) != 1:
        self.retry(countdown=60 * 5)
