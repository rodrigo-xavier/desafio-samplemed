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

    def remove_unique_keywords(self, request):
        # keywords = models.Keyword.list_keywords().exclude(name__in=request.data['keyword_set'].values())
        keywords_list = models.Keyword.list_keywords()
        for counter, keyword in enumerate(request.data['keyword_set']):
            if keywords_list.filter(name=keyword.get('name')).exists():
                request.data['keyword_set'].pop(counter)
        return request


    """
    Observações sobre a classe create:
    - Devido ao motivo de na classe Keyword, o atributo 'name' ser 'unique=True', o método 'create' abaixo,
    não permite prosseguir para o método 'create' do serializer, alegando que um objeto com esse 'name' já existe.
    Portanto, para contornar isso, foi preciso criar um método 'remove_unique_keywords' que irá remover de 'request'
    campos com objetos de mesmo nome já registrados no banco de dados, já que não é possível remover todo o campo.
    """
    def create(self, request, *args, **kwargs):
        
        user = request.user

        if user.article_set.count() >= 20 or len(request.data['keyword_set']) >= 7:
            return Response({'error': 'Exceeded limit of articles per user or keywords per article.'}, status=status.HTTP_400_BAD_REQUEST)

        keywords = [keyword.get('name') for keyword in request.data['keyword_set']]
        request.data['keywords'] = keywords
        # request = self.remove_unique_keywords(request)
        # print(request.data)
        
        return super().create(request, *args, **kwargs)
    
    def update(self, request, *args, **kwargs):

        # if article.exceeded_limit():
        #     return Response({'error': 'Exceeded limit of articles per user or keywords per article.'}, status=status.HTTP_400_BAD_REQUEST)

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

