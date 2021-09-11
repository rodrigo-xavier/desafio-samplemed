from blog import models
from rest_framework import serializers
from blog.models import User

class UserSerializer(serializers.ModelSerializer):
    """
    `QuestionViewSet` é uma viewset da `Question` model.
    provê criação de novas Perguntas e permite que o Player responda a uma pergunta.
    `question`, `user_answer`, `correct_answer`
    """
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
        
    class Meta:
        model = models.User
        fields = ['id', 'username', 'password']
        extra_kwargs = {
            "password": {"write_only": True},
        }

class KeywordSerializer(serializers.ModelSerializer):
    """
    `QuestionViewSet` é uma viewset da `Question` model.
    provê criação de novas Perguntas e permite que o Player responda a uma pergunta.
    `question`, `user_answer`, `correct_answer`
    """
    class Meta:
        model = models.Keyword
        fields = ['name']

class ArticleSerializer(serializers.ModelSerializer):
    """
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
        fields = ['title', 'subtitle', 'article_type', 'content', 'status', 'keyword_set']




