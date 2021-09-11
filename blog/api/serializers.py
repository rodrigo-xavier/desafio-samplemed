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
    keyword_set = KeywordSerializer(many=True, read_only=True)

    def set_keywords(self, article, keywords):
        for k in keywords:
            keyword, created = models.Keyword.objects.get_or_create(name=k)
            article.keyword_set.add(keyword)
    
    def create(self, validated_data):
        validated_data['author'] = self.context['request'].user
        article = models.Article.objects.create(**validated_data)
        keywords = self.context['request'].data['keywords']
        self.set_keywords(article, keywords)

        return article
    class Meta:
        model = models.Article
        fields = ['title', 'subtitle', 'article_type', 'content', 'status', 'keyword_set']




