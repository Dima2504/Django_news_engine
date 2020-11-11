from django.shortcuts import render

from allauth.account.views import LoginView
from django.conf import settings


class MyLoginView(LoginView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['TELEGRAM_BOT_USERNAME'] = settings.TELEGRAM_BOT_USERNAME
        return context

