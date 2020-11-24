from rest_framework import serializers

from .models import News, Category
from auth_system.models import User

from allauth.socialaccount.models import SocialAccount


class CategorySerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=False)

    class Meta:
        model = Category
        fields = ('name', 'slug',)


class NewsSerializer(serializers.ModelSerializer):
    category = CategorySerializer()

    class Meta:
        model = News
        fields = ('slug',
                  'title', 'description', 'author', 'source_name', 'url', 'url_to_image', 'published_at', 'content',
                  'category')


class UserSerializer(serializers.ModelSerializer):
    categories_email = CategorySerializer(many=True)
    categories_telegram = CategorySerializer(many=True)
    checked_news = serializers.SlugRelatedField(many=True, read_only=True, slug_field='slug')

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'categories_email', 'categories_telegram', 'send_news_to_email',
                  'countdown_to_email', 'send_news_to_telegram', 'countdown_to_telegram', 'checked_news')


class TelegramUserSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = SocialAccount
        fields = ('uid', 'last_login', 'user')
