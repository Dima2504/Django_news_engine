from django.shortcuts import redirect
from django.shortcuts import render


def news_redirect(request):
    return redirect('news:start', permanent=True)

from django.conf import settings
from django.shortcuts import reverse
def bot(request):
    return render(request, template_name='bot.html')
