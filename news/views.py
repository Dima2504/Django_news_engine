from django.shortcuts import render
from django.shortcuts import redirect
from django.views.generic.base import View
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.conf import settings

from .forms import PersonalPreferencesForm
from .models import Category
from .models import News


# Create your views here.


def index(request):
    articles = News.objects.all().only('title', 'description', 'published_at', 'url_to_image', 'slug')[:10]
    categories = Category.objects.all().only('name', 'slug')
    return render(request, template_name='news/index.html', context={'categories': categories, 'articles': articles})

def category_news(request, slug):
    category_articles = News.objects.filter(category__slug=slug).only('title', 'description', 'published_at', 'url_to_image', 'slug')[:10]
    categories = Category.objects.all().only('name', 'slug')
    return render(request, template_name='news/index.html', context={'categories': categories, 'articles': category_articles, 'selected_category_slug': slug})

class NewsDetail(DetailView):
    model = News
    context_object_name = 'article'


    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['categories'] = Category.objects.all()
        return context


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
