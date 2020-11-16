from django.urls import path

from .views import MyLoginView
from .views import DisconnectSocialAccountView

urlpatterns = [
    path('login/', MyLoginView.as_view(), name='account_login'),
    path('disconnect-social-account/', DisconnectSocialAccountView.as_view(), name='disconnect_social_account'),
]