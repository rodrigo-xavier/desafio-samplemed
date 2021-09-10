from blog import models
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ['id', 'username']

class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Article
        fields = ['title', 'subtitle', 'article_type', 'content', 'status', 'keyword']

class KeywordSerializer(serializers.ModelSerializer):
    article_title = serializers.CharField(source='article.title')
    class Meta:
        model = models.Keyword
        fields = ['article_title', 'tag']


