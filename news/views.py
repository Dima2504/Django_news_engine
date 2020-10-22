from django.shortcuts import render
from django.shortcuts import redirect
from django.views.generic.base import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.conf import settings

from .forms import PersonalPreferencesForm
from .models import Category

from newsapi import NewsApiClient
import datetime

# Create your views here.


def index(request):
    newsapi = NewsApiClient(api_key=settings.NEWSAPI_KEY)
    top_headlines = newsapi.get_top_headlines(country='ua')
    if top_headlines['status'] == 'ok':
        articles = top_headlines['articles']
        for article in articles:
            article['publishedAt'] = datetime.datetime.strptime(article['publishedAt'], '%Y-%m-%dT%H:%M:%SZ')
    else:
        articles = []
    categories = Category.objects.all()
    return render(request, template_name='news/index.html', context={'categories': categories, 'articles': articles})

class PersonalAccount(LoginRequiredMixin, View):

    def get(self, request):
        obj = request.user
        form = PersonalPreferencesForm()
        for category in obj.categories.all():
            form.initial[category.name] = True
        return render(request, template_name='news/personal_account.html', context={'user': obj, 'form': form})

    def post(self, request):
        user = request.user
        form = PersonalPreferencesForm(request.POST)
        if form.is_valid():
            categories = Category.objects.filter(name__in=form.changed_data)
            user.categories.clear()
            user.categories.set(categories, clear=True)
            messages.success(request, 'Дані успішно збережені!')
        return redirect('news:start')
