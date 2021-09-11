from blog import models
from rest_framework import viewsets
from rest_framework import permissions
from blog.api import serializers
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework import status
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import authentication_classes

class CustomerAccessPermission(permissions.BasePermission):
    """
    `CustomerAccessPermission` é uma viewset de `BasePermission`.
    Permite criar autenticação personalizada para acesso dos usuários.
    Não está sendo utilizado
    """

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
    `UserViewSet` é uma viewset da `User` model.
    Permite a criação de novos usuários
    search_fields - `username`
    """
    permission_classes = [IsAuthenticatedOrReadOnly]
    authentication_classes = [TokenAuthentication]
    serializer_class = serializers.UserSerializer
    filter_backends =  (SearchFilter, DjangoFilterBackend)
    filter_fields = ('id', 'username')
    search_fields = ('username')
    queryset = models.User.objects.all()

class ArticleViewSet(viewsets.ModelViewSet):
    """
    `ArticleViewSet` é uma viewset da `Article` model.
    permite a listagem de artigos, criação de novos artigos e a atualização de artigos existentes
    search_fields - `title` `subtitle` `article_type` `status` `keyword_set`
    methods: `create` valida se usuário não atingiu limite de artigos ou palavras chave e 
                      adciona uma lista de strings de keywords na request para enviar ao serializer
    """
    permission_classes = [IsAuthenticatedOrReadOnly]
    authentication_classes = [TokenAuthentication]
    serializer_class = serializers.ArticleSerializer
    queryset = models.Article.objects.all()
    filter_backends =  (SearchFilter, DjangoFilterBackend)
    filter_fields = ('title', 'subtitle', 'article_type', 'status', 'keyword_set')
    search_fields = ('title', 'subtitle', 'article_type', 'status', 'keyword_set')

    def create(self, request, *args, **kwargs):
        user = request.user

        if user.article_set.count() >= 50 or len(request.data['keyword_set']) >= 7:
            return Response({'error': 'Exceeded limit of articles per user or keywords per article.'}, status=status.HTTP_400_BAD_REQUEST)

        keywords = [keyword.get('name') for keyword in request.data['keyword_set']]
        request.data['keywords'] = keywords
        
        return super().create(request, *args, **kwargs)

class KeywordViewSet(viewsets.ModelViewSet):
    """
    `KeywordViewSet` é uma viewset da `Keyword` model.
    permite listar, criar e atualizar keywords
    """
    permission_classes = [IsAuthenticatedOrReadOnly]
    authentication_classes = [TokenAuthentication]
    serializer_class = serializers.KeywordSerializer
    queryset = models.Keyword.objects.all()

