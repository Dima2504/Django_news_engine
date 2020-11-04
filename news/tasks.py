from news_engine import celery_app

from .service import pick_top_headlines
from .service import delete_old_news_from_db
from .service import get_users_needed_news_contained_into_signatures


from news.models import History
from celery import chain
from celery import group
from django.core.mail import send_mail
from django.conf import settings

@celery_app.task
def pick_beat_news():
    pick_top_headlines()


@celery_app.task
def clear_db():
    delete_old_news_from_db()


@celery_app.task
def send_one_news_to_user(subject, message, news_id, user_id, user_email):
    send_mail(subject, message, from_email=settings.DEFAULT_FROM_EMAIL, recipient_list=[user_email,])
    History.objects.create(user_id=user_id, news_id=news_id, is_checked_on_site=False, is_checked_on_email=True)


@celery_app.task
def send():
    tasks = get_users_needed_news_contained_into_signatures()
    group([chain(*t) for t in tasks.values()]).apply_async()