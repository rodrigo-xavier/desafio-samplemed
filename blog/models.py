from django.conf import settings
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _

class User(AbstractUser):
    """ 
    Observations: Em um projeto maior, o indicado seria criar um app apenas
    para o tratamento de usuários e grupos do sistema
    """

    def __str__(self):
        return self.username
    
    class Meta:
        permissions = [
            ('can_create_articles', _("Can register articles in blog")),
        ]

class Article(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_("User"))
    title = models.CharField(verbose_name=_("Title"), max_length=200)
    subtitle = models.CharField(verbose_name=_("Sub Title"), max_length=200)
    content = models.TextField(verbose_name=_("Content"), max_length=2000)
    keyword_set = models.TextField(verbose_name=_("Keyword Set"), max_length=200)
    article_type = models.PositiveSmallIntegerField(verbose_name=_("Type"), default=0, blank=True)
    status = models.PositiveSmallIntegerField(verbose_name=_("Status"), default=0, blank=True)
    created_date = models.DateTimeField(verbose_name=_("Created Date"), default=timezone.now)
    published_date = models.DateTimeField(verbose_name=_("Published Date"), blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title + " - " + self.subtitle