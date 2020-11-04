import time
from django.views.generic.base import View
from django.core.paginator import Paginator
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render

from allauth.account.models import EmailAddress
from allauth.account.utils import send_email_confirmation

def unique_slug():
    return str(time.time()).replace('.', '')

class NewsListAjaxMixin(View):
    required_fields = ('title', 'published_at', 'url_to_image', 'slug')
    articles = None
    categories = None
    addition_context_data = {}
    def get(self, request):
        if request.is_ajax():
            page_num = request.GET['page']
            page = Paginator(self.articles, settings.NEWS_PER_PAGE).get_page(page_num)
            object_list = list(page.object_list)
            return JsonResponse({'data': object_list, 'has_next': page.has_next()})
        else:
            articles = Paginator(self.articles, settings.NEWS_PER_PAGE).get_page(1).object_list
            return render(request, template_name='news/index.html',
                          context={'categories': self.categories, 'articles': articles, **self.addition_context_data})


class VerifiedEmailRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        if not EmailAddress.objects.filter(user=request.user,
                                           verified=True).exists():
            send_email_confirmation(request, request.user)
            return render(request,
                          'account/verified_email_required.html')
        return super().dispatch(request, *args, **kwargs)