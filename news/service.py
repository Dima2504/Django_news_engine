from newsapi import NewsApiClient
from newsapi.const import categories
from django.utils import timezone
from django.conf import settings
from django.core.mail import send_mail
from django.utils.timezone import make_aware

import datetime
import logging

from auth_system.models import User
from news.models import History
from news.models import News, Category
import requests

logger = logging.getLogger('news.tasks')


def pick_top_headlines():
    newsapi = NewsApiClient(api_key=settings.NEWS_API_KEY)
    for category in categories:
        top = newsapi.get_top_headlines(country='ua',
                                        category=category)
        logger.info(f'receive top headlines in {category}')
        category_obj = Category.objects.get(slug=category)
        if top['status'] == 'ok':
            articles = top['articles']
            news = []
            for article in articles:
                one_news = News(category=category_obj,
                                author=article['author'] or '',
                                title=article['title'] or '',
                                description=article['description'] or '',
                                url=article['url'] or '',
                                url_to_image=article['urlToImage'] or '',
                                published_at=make_aware(
                                    datetime.datetime.strptime(article['publishedAt'], '%Y-%m-%dT%H:%M:%SZ')),
                                content=article['content'] or '', )
                news.append(one_news)
            News.objects.bulk_create(news, ignore_conflicts=True)
            logger.info(f'save received news in {category} to db')


def delete_old_news_from_db():
    News.objects.filter(
        id__in=list(News.objects.values_list('pk', flat=True)[settings.NEWS_TO_SAVE_AFTER_CLEAN:])).delete()
    logger.info('Successful delete')


def send_one_news_to_one_user(user_id):
    user = User.objects.get(id=user_id)
    news = News.objects.exclude(users_saw=user).filter(category__in=user.categories_email.all()).last()
    if send_mail(news.title, news.description, from_email=settings.DEFAULT_FROM_EMAIL,
                 recipient_list=[user.email, ]) == 1:
        logger.info(f'User {user.email} receive news {news.id} on email')
        History.objects.update_or_create(user_id=user_id, news_id=news.id, defaults={'checked_on': History.ON_EMAIL})
        logger.info(f'Create relationship with user {user.email} and news {news.id}')
    else:
        logging.warning(f'{user.email} did not receive {news.id}')


def generate_news_caption(news: News):
    title = f'<b>{news.title}</b>\n\n'
    description = news.description
    url = '<i><b>\n\nПосилання на оригінал: \n</b></i>' + news.url
    time = f'\n\n<pre>{timezone.localtime(news.published_at).strftime("%A, %d. %B %Y %I:%M%p")}</pre>'
    return title + description + url + time


def send_one_news_on_telegram(user_id, telegram_id):
    user = User.objects.get(id=user_id)
    news = News.objects.exclude(users_saw=user).filter(category__in=user.categories_telegram.all()).last()
    if news.url_to_image:
        response = requests.post(f'https://api.telegram.org/bot{settings.SOCIALACCOUNT_PROVIDERS["custom_telegram"]["TOKEN"]}/sendPhoto', data={'chat_id': telegram_id, 'photo': news.url_to_image, 'caption': generate_news_caption(news), 'parse_mode': 'HTML'}).json()
    else:
        response = requests.post(f'https://api.telegram.org/bot{settings.SOCIALACCOUNT_PROVIDERS["custom_telegram"]["TOKEN"]}/sendMessage', data={'chat_id': telegram_id, 'text': news.title + '\n\n' + generate_news_caption(news)}).json()
    if response['ok']:
        logger.info(f'User {user.email} receive news {news.id} on email')
        History.objects.update_or_create(user_id=user_id, news_id=news.id, defaults={'checked_on': History.ON_TELEGRAM})
        logger.info(f'Create relationship with user {user.email} and news {news.id}')
    else:
        logging.warning(f'{user.email} did not receive {news.id}: {response["description"]}')
