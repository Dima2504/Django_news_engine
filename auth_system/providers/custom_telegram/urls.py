from django.urls import path

from . import views


urlpatterns = [path("telegram/login/", views.telegram_login, name="custom_telegram_login")]