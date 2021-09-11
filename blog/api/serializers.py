from blog import models
from rest_framework import serializers
from blog.models import User

class UserSerializer(serializers.ModelSerializer):
    """
    `UserViewSet` é uma viewset da `User` model.
    `usename`, `password`
    """
        
    class Meta:
        model = models.User
        fields = ['id', 'username', 'password']
        extra_kwargs = {
            "password": {"write_only": True},
        }

class KeywordSerializer(serializers.ModelSerializer):
    """
    `UserViewSet` é uma viewset da `User` model.
    `name`
    """
    class Meta:
        model = models.Keyword
        fields = ['name']

class ArticleSerializer(serializers.ModelSerializer):
    """
    `ArticleViewSet` é uma viewset da `Article` model.
    methods: `set_keywords` - cria se não existe e pega se existe, um objeto com uma keyword e adiciona 
                              as keywords no artigo 
    observations: Foi necessário definir keyword_set como read_only, porque do contrário, a implementação
    causava conflitos com `unique=True` no atributo `name` de `Keywords`. Conflitos estes que possuem dificuldade
    acentuada para serem solucionados.
    """
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
        fields = ['id', 'title', 'subtitle', 'article_type', 'content', 'status', 'keyword_set']




