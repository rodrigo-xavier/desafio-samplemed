from blog import models
from rest_framework import viewsets
from rest_framework import permissions
from blog.api import serializers
from rest_framework.filters import SearchFilter
from django.core.exceptions import PermissionDenied
import random

class UserViewSet(viewsets.ModelViewSet):
    """
    `UserViewSet` é a viewset de `User` model.
    """
    serializer_class = serializers.UserSerializer
    filter_backends =  (SearchFilter,)
    filter_fields = ('id', 'username')
    search_fields = ('username')
    queryset = models.User.objects.all()

class ArticleViewSet(viewsets.ModelViewSet):
    """
    `ArticleViewSet` é uma viewset da `Article` model.
    """
    serializer_class = serializers.ArticleSerializer
    queryset = models.Article.objects.all()
    filter_backends =  (SearchFilter,)
    filter_fields = ('title', 'subtitle', 'article_type', 'content', 'status', 'keyword_set')
    search_fields = ('title', 'subtitle', 'article_type', 'content', 'status', 'keyword_set')
    
    def create(self, request, *args, **kwargs):
        if request.user.admin:
            return super().create(request, *args, **kwargs)
    
    def update(self, request, *args, **kwargs):
        if request.user.admin:
            return super().create(request, *args, **kwargs)
