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
    TYPE = [
        (0, _('Science')),
        (1, _('Technology')),
        (2, _('Medical')),
        (3, _('Enterteinment')),
        (4, _('Fiction')),
        (5, _('Other')),
    ]
    STATUS = [
        (0, _('Created')),
        (1, _('On Approval')),
        (2, _('Published')),
        (3, _('Not Approved')),
    ]

    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name=_("User"))
    title = models.CharField(verbose_name=_("Title"), max_length=200, default='', blank=False, null=False)
    subtitle = models.CharField(verbose_name=_("Sub Title"), max_length=200, blank=True)
    content = models.TextField(verbose_name=_("Content"), max_length=2000, blank=True)
    created_date = models.DateTimeField(verbose_name=_("Created Date"), default=timezone.now, null=False)
    published_date = models.DateTimeField(verbose_name=_("Published Date"), blank=True, null=True)
    article_type = models.PositiveSmallIntegerField(choices=TYPE, verbose_name=_("Type"), default=0, null=False)
    status = models.PositiveSmallIntegerField(choices=STATUS, verbose_name=_("Status"), default=0, null=False)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        if self.subtitle:
            return self.title + " - " + self.subtitle
        return self.title

class Keyword(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, verbose_name=_("Article"))
    tag = models.CharField(verbose_name=_("Keyword Set"), max_length=30)

    def __str__(self):
        return str(self.article.title) + " - " + str(self.tag)