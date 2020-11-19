from rest_framework.serializers import ModelSerializer

from .models import News, Category


class CategorySerializer(ModelSerializer):

    class Meta:
        model = Category
        fields = ('name', 'slug',)


class NewsListSerializer(ModelSerializer):
    category = CategorySerializer()

    class Meta:
        model = News
        fields = ('title', 'description', 'author', 'source_name', 'url', 'url_to_image', 'published_at', 'content', 'category')
