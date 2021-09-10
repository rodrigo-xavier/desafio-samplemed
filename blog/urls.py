from django.urls import path, re_path
from rest_framework import routers
from django.conf.urls import include
from blog.api import viewsets
from rest_framework.authtoken import views

app_name = 'blog'

router = routers.DefaultRouter()
router.register(r'article', viewsets.ArticleViewSet, basename='Article')
router.register(r'user', viewsets.UserViewSet, basename='User')

urlpatterns = [
    path('api/', include(router.urls), name='api'),
    path('api-token-auth/', views.obtain_auth_token),
]