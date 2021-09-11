from blog import models
from rest_framework import viewsets
from rest_framework import permissions
from blog.api import serializers
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response


class CustomerAccessPermission(permissions.BasePermission):
    message = 'Adding customers not allowed.'

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            return True
        return False

class UserViewSet(viewsets.ModelViewSet):
    """
    `UserViewSet` é a viewset de `User` model.
    """
    # permission_classes = [CustomerAccessPermission]
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.UserSerializer
    filter_backends =  (SearchFilter,)
    filter_fields = ('id', 'username')
    search_fields = ('username')
    queryset = models.User.objects.all()

class ArticleViewSet(viewsets.ModelViewSet):
    """
    `ArticleViewSet` é uma viewset da `Article` model.
    """
    # permission_classes = [CustomerAccessPermission]
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.ArticleSerializer
    queryset = models.Article.objects.all()
    filter_backends =  (SearchFilter,)
    filter_fields = ('title', 'subtitle', 'article_type', 'status')
    search_fields = ('title', 'subtitle', 'article_type', 'status')
    
    # def list(self, request, *args, **kwargs):
    #     article = request.GET.get('test')
    #     return super().list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        article = request.POST.get('article')

        if article.exceeded_limit() and request.POST.get('keyword_set').count() >= 5:
            return Response({'error': 'Exceeded limit of articles per user or keywords per article.'}, status=status.HTTP_400_BAD_REQUEST)
            
        return super().create(request, *args, **kwargs)
    
    def update(self, request, *args, **kwargs):
        article = request.POST.get('article')

        if article.exceeded_limit():
            return Response({'error': 'Exceeded limit of articles per user or keywords per article.'}, status=status.HTTP_400_BAD_REQUEST)

        return super().create(request, *args, **kwargs)

class KeywordViewSet(viewsets.ModelViewSet):
    """
    `KeywordViewSet` é uma viewset da `Keyword` model.
    """
    permission_classes = [CustomerAccessPermission]
    serializer_class = serializers.KeywordSerializer
    queryset = models.Keyword.objects.all()
    filter_backends =  (SearchFilter,)
    filter_fields = ('name')
    search_fields = ('name')

