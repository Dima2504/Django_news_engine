from django.urls import path

from . import views


urlpatterns = [path("telegram/login/", views.telegram_login, name="custom_telegram_login"),
               path("telegram/login/connect", views.telegram_connect, name="custom_telegram_connect"), ]
