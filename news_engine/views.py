from django.shortcuts import redirect


def news_redirect(request):
    return redirect('news:start', permanent=True)