from django.urls import path
from .views import *

app_name = 'news'

urlpatterns = [
    path('', AllNews.as_view(), name='start'),
    path('personal-account/', PersonalAccount.as_view(), name='personal_account'),
    path('news-history/', NewsHistory.as_view(), name='news_history'),
    path('ajax-filter/', ajax_filter, name='ajax_filter'),
    path('<slug:slug>/', CategoryNews.as_view(), name='category_news'),
    path('detail/<slug:slug>/', NewsDetail.as_view(), name='news_detail'),
]