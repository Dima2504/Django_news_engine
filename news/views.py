from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.http import HttpResponse
from django.views.generic.base import View
from django.contrib.auth.mixins import LoginRequiredMixin


# Create your views here.

def index(request):
    return render(request, template_name='news/index.html')

class PersonalAccount(LoginRequiredMixin, View):

    def get(self, request):
        return render(request, template_name='news/personal_account.html', context={'user': request.user})
