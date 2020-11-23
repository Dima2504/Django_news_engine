from django.urls import path, include
from .views import *
import news.api_views as api

app_name = 'news'

urlpatterns = [
    path('', AllNews.as_view(), name='start'),
    path('api/news/', api.NewsListView.as_view(), name='api_news_list'),
    path('api/news/<slug:slug>/', api.NewsDetailView.as_view(), name='api_news_detail'),
    path('api/users/', api.UsersListView.as_view(), name='api_users_list'),
    path('api/telegram-users/', api.TelegramUsersListView.as_view(), name='api_telegram_users_list'),
    path('api/telegram-users/<int:telegram_id>/', api.UserDetailView.as_view(), name='api_user_detail'),

    path('personal-account/', PersonalAccount.as_view(), name='personal_account'),
    path('news-history/', NewsHistory.as_view(), name='news_history'),
    path('ajax-filter/', AjaxFilter.as_view(), name='ajax_filter'),
    path('<slug:slug>/', CategoryNews.as_view(), name='category_news'),
    path('detail/<slug:slug>/', NewsDetail.as_view(), name='news_detail'),
]
