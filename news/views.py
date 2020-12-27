from django.shortcuts import render
from django.shortcuts import redirect
from django.views.generic.base import View
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.conf import settings

from django.http import JsonResponse, HttpResponseNotFound
from django.db.models import Q

from .forms import PersonalPreferencesForm

from .models import Category
from .models import News
from .models import History

from allauth.socialaccount.models import SocialAccount

from .utils import NewsListAjaxMixin
from .utils import VerifiedEmailRequiredMixin

import datetime
import logging

logger = logging.getLogger(__name__)


# Create your views here.

class AllNews(NewsListAjaxMixin, View):
    def get(self, request):
        if request.user.is_anonymous:
            self.articles = News.objects.all().values(*self.required_fields)
            logger.debug('Anonymous user in Allnews')
        else:
            self.articles = News.objects.all().values(*self.required_fields).difference(
                request.user.checked_news.all().values(*self.required_fields)).order_by('-published_at')
            logger.debug(f'User: {request.user.id} in Allnews')

        self.categories = Category.objects.filter(is_main=True).only('name', 'slug')
        return super().get(request)


class CategoryNews(NewsListAjaxMixin, View):

    def get(self, request, slug):

        if request.user.is_anonymous:
            self.articles = News.objects.filter(category__slug=slug).values(*self.required_fields)
            logger.debug(f'Anonymous user in category {slug}')
        else:
            self.articles = News.objects.filter(category__slug=slug).values(*self.required_fields).difference(
                request.user.checked_news.filter(category__slug=slug).values(*self.required_fields)).order_by(
                '-published_at')
            logger.debug(f'User: {request.user.id} if category {slug}')

        self.categories = Category.objects.filter(is_main=True).only('name', 'slug')
        self.addition_context_data = {'selected_category_slug': slug,
                                      'selected_category_name': Category.objects.get(slug=slug).name}
        return super().get(request)

from .models import cohensutherland
import requests

class NewsDetail(DetailView):
    model = News
    context_object_name = 'article'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['categories'] = Category.objects.all()
        return context

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        if not request.user.is_anonymous:
            History.objects.get_or_create(user=request.user, news=self.object)
            logger.debug(f'User: {request.user.id} see news {self.object.id}')
        logger.debug(f'Anonymous user see news {self.object.id}')

        image = request.get(self.object.url_to_image).content
        resronse = cohensutherland(image=image, 0, 100, 100, 0, 1, 4, 5, 6)
        return response, 


class PersonalAccount(LoginRequiredMixin, VerifiedEmailRequiredMixin, View):

    def get(self, request):
        user = request.user
        logger.debug(f'User {user.id} in personal account GET')
        form = PersonalPreferencesForm()
        for category in user.categories_email.filter(is_main=True).only('slug'):
            form.initial[category.slug+'_email'] = True
        for category in user.categories_telegram.filter(is_main=True).only('slug'):
            form.initial[category.slug+'_telegram'] = True

        form.initial['send_news_to_email'] = user.send_news_to_email
        form.initial['countdown_to_email'] = user.countdown_to_email.seconds / 60

        form.initial['send_news_to_telegram'] = user.send_news_to_telegram
        form.initial['countdown_to_telegram'] = user.countdown_to_telegram.seconds / 60

        social_accounts = SocialAccount.objects.filter(user=user).only('provider')

        return render(request, template_name='news/personal_account.html',
                      context={'form': form, 'TELEGRAM_BOT_USERNAME': settings.TELEGRAM_BOT_USERNAME, **{social_account.provider + "_account_id": social_account.id for social_account in social_accounts}})

    def post(self, request):
        user = request.user
        logger.debug(f'User {user.id} in personal account POST')
        form = PersonalPreferencesForm(request.POST)
        if form.is_valid():


            changed_data_email = [field[:-6] for field in form.changed_data if field.endswith('_email')]
            changed_data_telegram = [field[:-9] for field in form.changed_data if field.endswith('_telegram')]


            categories = Category.objects.filter(slug__in=changed_data_email)
            user.categories_email.set(categories, clear=True)

            categories = Category.objects.filter(slug__in=changed_data_telegram)
            user.categories_telegram.set(categories, clear=True)

            user.countdown_to_email = datetime.timedelta(minutes=int(form.cleaned_data['countdown_to_email']))
            user.send_news_to_email = form.cleaned_data['send_news_to_email']


            user.countdown_to_telegram = datetime.timedelta(minutes=int(form.cleaned_data['countdown_to_telegram']))
            if SocialAccount.objects.filter(user=user).exists():
                user.send_news_to_telegram = form.cleaned_data['send_news_to_telegram']

            user.save()
            messages.success(request, 'Дані успішно збережені!')
        return redirect('news:start')


class NewsHistory(LoginRequiredMixin, View):
    def get(self, request):
        categories = Category.objects.filter(is_main=True).only('name', 'slug')
        articles = request.user.checked_news.all().values('title', 'published_at', 'url_to_image', 'slug')
        return render(request, template_name='news/news_history.html', context={'categories': categories, 'articles': articles})

def Rabin_Karp_Matcher(text, pattern, d, q):
       n = len(text)
       m = len(pattern)
       h = pow(d,m-1)%q
       p = 0
       t =0
       result = []
       for i in range(m):
           p = (d*p+ord(pattern[i]))%q
           t = (d*t+ord(text[i]))%q
       for s in range(n-m):
           if p == t:
               match = True
               for i in range(m):
                   if pattern[i] != text[s+i]:
                       match = False
                       break
               if match:
                   result = result + [s]
           if s < n-m:
                   t = (d*(t-ord(text[s+1])*h)+ord(text[s+m]))%q
       return result

def quicksort(nums, fst, lst):
		if fst >= lst: return
		i, j = fst, lst
		pivot = nums[(fst + lst) // 2]
		while i <= j:
			while nums[i] < pivot: i += 1
			while nums[j] > pivot: j -= 1
			if i <= j:
				nums[i], nums[j] = nums[j], nums[i]
				i, j = i + 1, j - 1
		quicksort(nums, fst, j)
		quicksort(nums, i, lst)
	return nums

class AjaxFilter(View):
    def get(self, request):
        if request.is_ajax():
            articles = request.user.checked_news.filter(Q(title__icontains=request.GET.get('text')) | Q(description__icontains=request.GET.get('text')))
            articles = articles.filter(history__checked_on__in=request.GET.getlist('checked-on'))
            resualt = []
            for a in articles:
                res.append(Rabin_Karp_Matcher(a.description, request.GET.getlist('checked-on'), 1, 0))
            if request.GET.get('category') != 'all':
                articles = articles.filter(category__slug=request.GET.get('category'))
            sort_by = request.GET.get('sort-by')
            order = request.GET.get('order', '')
            articies = [article.checked_at.hour for article in articles]
            articies = quicksort(articies, 1, 10)

            if sort_by == 'checked_at':
                articles = articles.order_by(order+'history__checked_at')
            elif sort_by == 'published_at':
                articles = articles.order_by(order+'published_at')
            elif sort_by == 'text':
                articles = articles.order_by(order+'title', order+'description')
            articles = articles.values('title', 'published_at', 'url_to_image', 'slug')
            return JsonResponse({'data': list(articles)})
        else:
            return HttpResponseNotFound()
        return resualt
