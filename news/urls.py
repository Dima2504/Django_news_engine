from django.urls import path, include
from .views import *
from .api_views import NewsListView

app_name = 'news'

urlpatterns = [
    path('', AllNews.as_view(), name='start'),
    path('api/news-list/', NewsListView.as_view(), name='news-list'),  # TODO need to be changed

    path('personal-account/', PersonalAccount.as_view(), name='personal_account'),
    path('news-history/', NewsHistory.as_view(), name='news_history'),
    path('ajax-filter/', AjaxFilter.as_view(), name='ajax_filter'),
    path('<slug:slug>/', CategoryNews.as_view(), name='category_news'),
    path('detail/<slug:slug>/', NewsDetail.as_view(), name='news_detail'),
]
