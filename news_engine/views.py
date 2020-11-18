from django.shortcuts import redirect
from django.shortcuts import render


def news_redirect(request):
    return redirect('news:start', permanent=True)

