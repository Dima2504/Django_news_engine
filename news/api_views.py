from rest_framework.views import APIView
from rest_framework.response import Response
from .models import News
from .serializers import NewsListSerializer

from django.shortcuts import get_list_or_404


class NewsListView(APIView):
    def get(self, request):
        if 'category' in request.query_params:
            news = get_list_or_404(News, category__slug__in=request.query_params.getlist('category'))
        else:
            news = News.objects.all()
        if 'limit' in request.query_params:
            news = news[:int(request.query_params.get('limit'))]
        serializer = NewsListSerializer(news, many=True)
        return Response(serializer.data)