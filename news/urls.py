from django.urls import path
from .views import *

app_name = 'news'

urlpatterns = [
    path('', index, name='start'),
    path('personal-account/', PersonalAccount.as_view(), name='personal_account'),
    path('<slug:slug>/', category_news, name='category_news'),

]