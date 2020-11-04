from news.models import News, Category
from newsapi import NewsApiClient
from newsapi.const import categories
from django.conf import settings
from django.utils.timezone import make_aware
import datetime


from auth_system.models import User
from allauth.account.models import EmailAddress
from .tasks import send_one_news_to_user


def pick_top_headlines():
    newsapi = NewsApiClient(api_key=settings.NEWS_API_KEY)
    for category in categories:
        top = newsapi.get_top_headlines(country='ua',
                                        category=category)
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
                                published_at=make_aware(datetime.datetime.strptime(article['publishedAt'], '%Y-%m-%dT%H:%M:%SZ')),
                                content=article['content'] or '',)
                news.append(one_news)
            News.objects.bulk_create(news, ignore_conflicts=True)


def delete_old_news_from_db():
    News.objects.filter(id__in=list(News.objects.values_list('pk', flat=True)[settings.NEWS_TO_SAVE_AFTER_CLEAN:])).delete()


def get_users_needed_news_contained_into_signatures():
    """
    :return: dictionary where key - user id, values - list of ready celery signatures from task 'send_one_news_to_user'.
    """
    tasks = {}
    for news in News.objects.all().order_by('published_at'):
        title = news.title
        des = news.description
        users_ids_emails = User.objects.exclude(checked_news=news).filter(send_news_to_email=True,
                                                                          categories=news.category).values_list('id',
                                                                                                                'email')
        if users_ids_emails:
            for user_id, user_email in users_ids_emails:
                if not user_id in tasks:
                    tasks[user_id] = [
                        send_one_news_to_user.signature((title, des, news.id, user_id, user_email), countdown=10,
                                                        immutable=True), ]
                else:
                    tasks[user_id].append(
                        send_one_news_to_user.signature((title, des, news.id, user_id, user_email), countdown=10,
                                                        immutable=True))
