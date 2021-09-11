from blog import models
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ['id', 'username']

class KeywordSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Keyword
        fields = ['name']

class ArticleSerializer(serializers.ModelSerializer):
    keyword_set = KeywordSerializer(many=True)
    class Meta:
        model = models.Article
        fields = ['title', 'subtitle', 'article_type', 'content', 'status', 'keyword_set']



