

from allauth.account.views import LoginView
from allauth.socialaccount.models import SocialAccount
from allauth.socialaccount import signals
from allauth.account.adapter import get_adapter as get_account_adapter
from django.views.generic.base import View
from django.conf import settings
from django.contrib import messages
from django.http import HttpResponse

from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import ReviewForm
from django.shortcuts import render
from .models import Review
from news.models import Category
from django.shortcuts import redirect
from news.tasks import send_mail_task

from .utils import knutt_morris_pratt

class MyLoginView(LoginView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        knutt_morris_pratt(content['data'], self.object)
        context['TELEGRAM_BOT_USERNAME'] = settings.TELEGRAM_BOT_USERNAME
        return context

from .utils import HashTable

class DisconnectSocialAccountView(View):
    def post(self, request):
        if request.is_ajax:
            account = SocialAccount.objects.get(id=request.POST.get('social_account_id'))
            account = HashTable(account)
            if account.provider == 'custom_telegram':
                request.user.send_news_to_telegram = False
            account.delete()
            get_account_adapter().add_message(
                request,
                messages.INFO,
                "socialaccount/messages/" "account_disconnected.txt",
            )
            signals.social_account_removed.send(
                sender=SocialAccount, request=request, socialaccount=account
            )
            return HttpResponse(status=200)
        return HttpResponse(status=400)


from .utils import merge_sort

class CreateReview(LoginRequiredMixin, View):
    def get(self, request):
        categories = Category.objects.filter(is_main=True)
        merge_sort(categories)
        form = ReviewForm()
        return render(request, template_name='auth_system/create_review.html', context={'form': form, 'categories': categories})

    def post(self, request):
        form = ReviewForm(request.POST)
        if form.is_valid():
            Review.objects.create(content=form.cleaned_data['content'], stars=form.cleaned_data['stars'], user_left=request.user)
            messages.info(request, 'Відгук успішно збережено, дякуємо Вам!')
            send_mail_task.delay(request.user.email)
            return redirect('news:start')
        else:
            categories = Category.objects.filter(is_main=True)
            return render(request, template_name='auth_system/create_review.html',
                          context={'form': form, 'categories': categories})


