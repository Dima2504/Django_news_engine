from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_202_ACCEPTED, HTTP_404_NOT_FOUND
from .models import News
from .serializers import CategorySerializer, UserSerializer, NewsSerializer, \
    TelegramUserSerializer

from django.shortcuts import get_list_or_404

from auth_system.models import User

from allauth.socialaccount.models import SocialAccount


class NewsListView(APIView):
    def get(self, request):
        if 'category' in request.query_params:
            news = get_list_or_404(News, category__slug__in=request.query_params.getlist('category'))
        else:
            news = News.objects.all()
        if 'limit' in request.query_params:
            news = news[:int(request.query_params.get('limit'))]
        serializer = NewsSerializer(news, many=True)
        return Response(serializer.data)

class NewsDetailView(APIView):
    def get(self, request, slug):
        try:
            news = News.objects.get(slug=slug)
            serializer = NewsSerializer(news)
            return Response(serializer.data)
        except News.DoesNotExist as e:
            return Response(status=HTTP_404_NOT_FOUND, exception=e,
                            data={'details': 'News with such slug does not exist'})


class UsersListView(APIView):
    def get(self, request):
        serializer = UserSerializer(User.objects.exclude(is_staff=True), many=True)
        return Response(serializer.data)


class TelegramUsersListView(APIView):
    def get(self, request):
        serializer = TelegramUserSerializer(
            SocialAccount.objects.filter(provider='custom_telegram'), many=True)
        return Response(serializer.data)


class UserDetailView(APIView):
    def get(self, request, telegram_id):
        try:
            user = SocialAccount.objects.get(uid=telegram_id).user
            serializer = UserSerializer(user)
            return Response(serializer.data)
        except SocialAccount.DoesNotExist as e:
            return Response(status=HTTP_404_NOT_FOUND, exception=e,
                            data={'details': 'User with such telegram id does not exist'})