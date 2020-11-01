
from news.models import News, Category
from newsapi import NewsApiClient
from newsapi.const import categories
from django.conf import settings
from django.utils.timezone import make_aware
import datetime



def pick_top_headlines():
    newsapi = NewsApiClient(api_key=settings.NEWSAPI_KEY)
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