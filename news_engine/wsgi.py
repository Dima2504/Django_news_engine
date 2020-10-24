"""
WSGI config for news_engine project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
from threading import Thread



def pick_top_headlines():
    from news.models import News, Category
    from newsapi import NewsApiClient
    from django.conf import settings
    from django.utils.timezone import make_aware
    import datetime
    import time
    newsapi = NewsApiClient(api_key=settings.NEWSAPI_KEY)
    while True:
        top = newsapi.get_top_headlines(country='ua')
        general_category = Category.objects.get(slug='general')
        if top['status'] == 'ok':
            articles = top['articles']
            news = []
            for article in articles:
                one_news = News(category=general_category,
                                author=article['author'] or '',
                                title=article['title'] or '',
                                description=article['description'] or '',
                                url=article['url'] or '',
                                url_to_image=article['urlToImage'] or '',
                                published_at=make_aware(datetime.datetime.strptime(article['publishedAt'], '%Y-%m-%dT%H:%M:%SZ')),
                                content=article['content'] or '',)
                news.append(one_news)
            News.objects.bulk_create(news, ignore_conflicts=True)
        time.sleep(settings.NEWSAPI_TIMEDELTA_MINUTES*60)


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'news_engine.settings')

application = get_wsgi_application()

Thread(target=pick_top_headlines).start()
