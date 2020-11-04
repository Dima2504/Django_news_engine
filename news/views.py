from django.shortcuts import render
from django.shortcuts import redirect
from django.views.generic.base import View
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages


from .forms import PersonalPreferencesForm

from .models import Category
from .models import News
from .models import History

from .utils import NewsListAjaxMixin
from .utils import VerifiedEmailRequiredMixin

import datetime

# Create your views here.

class AllNews(NewsListAjaxMixin, View):
    def get(self, request):
        if request.user.is_anonymous:
            self.articles = News.objects.all().values(*self.required_fields)
        else:
            self.articles = News.objects.all().values(*self.required_fields).difference(
                request.user.checked_news.all().values(*self.required_fields)).order_by('-published_at')

        self.categories = Category.objects.filter(is_main=True).only('name', 'slug')
        return super().get(request)


class CategoryNews(NewsListAjaxMixin, View):

    def get(self, request, slug):

        if request.user.is_anonymous:
            self.articles = News.objects.filter(category__slug=slug).values(*self.required_fields)
        else:
            self.articles = News.objects.filter(category__slug=slug).values(*self.required_fields).difference(
                request.user.checked_news.filter(category__slug=slug).values(*self.required_fields)).order_by(
                '-published_at')

        self.categories = Category.objects.filter(is_main=True).only('name', 'slug')
        self.addition_context_data = {'selected_category_slug': slug,
                                      'selected_category_name': Category.objects.get(slug=slug).name}
        return super().get(request)


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
            History.objects.create(user=request.user, news=self.object)
        return response


class PersonalAccount(LoginRequiredMixin, VerifiedEmailRequiredMixin, View):

    def get(self, request):
        user = request.user
        form = PersonalPreferencesForm()
        for category in user.categories.filter(is_main=True).only('slug'):
            form.initial[category.slug] = True
        form.initial['send_news_to_email'] = user.send_news_to_email
        form.initial['countdown_to_email'] = user.countdown_to_email.seconds / 60
        return render(request, template_name='news/personal_account.html', context={'form': form})

    def post(self, request):
        user = request.user
        form = PersonalPreferencesForm(request.POST)
        if form.is_valid():
            categories = Category.objects.filter(slug__in=form.changed_data)
            user.categories.set(categories, clear=True)
            user.send_news_to_email = form.cleaned_data['send_news_to_email']
            user.countdown_to_email = datetime.timedelta(minutes=int(form.cleaned_data['countdown_to_email']))
            user.save()
            messages.success(request, 'Дані успішно збережені!')
        return redirect('news:start')
