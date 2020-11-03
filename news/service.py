from news.models import News, Category
from newsapi import NewsApiClient
from newsapi.const import categories
from django.conf import settings
from django.utils.timezone import make_aware
import datetime

from django.core.mail import send_mass_mail
from auth_system.models import User


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


# def send():
#     # for user in User.objects.select_related().filter(send_news_to_email=True):
#     #     News.objects.exclude(user_saw=user).filter(category__in=user.categories).order_by('published_at')
#     for news in News.objects.select_related().all().order_by('published_at'):
