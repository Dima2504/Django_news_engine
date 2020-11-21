

from allauth.account.views import LoginView
from allauth.socialaccount.models import SocialAccount
from allauth.socialaccount import signals
from allauth.account.adapter import get_adapter as get_account_adapter
from django.views.generic.base import View
from django.conf import settings
from django.contrib import messages
from django.http import HttpResponse

class MyLoginView(LoginView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['TELEGRAM_BOT_USERNAME'] = settings.TELEGRAM_BOT_USERNAME
        return context


class DisconnectSocialAccountView(View):
    def post(self, request):
        if request.is_ajax:
            account = SocialAccount.objects.get(id=request.POST.get('social_account_id'))
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