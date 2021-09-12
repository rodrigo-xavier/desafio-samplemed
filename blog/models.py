from django.conf import settings
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError

class User(AbstractUser):
    """ 
    Observations: Em um projeto maior, o indicado seria criar um app apenas
    para o tratamento de usuários e grupos do sistema
    Não está sendo utilizado
    """

    def __str__(self):
        return self.username
    
    class Meta:
        permissions = [
            ('can_create_articles', _("Can register articles in blog")),
        ]

class Keyword(models.Model):
    """
    `Keyword` model.
    Funciona como uma tag dos conteúdos abordados por um artigo.
    attributes: `name`
    methods: `list_keywords`: Lista todas as keywords cadastradas
    """
    
    name = models.CharField(verbose_name=_("Keyword Set"), max_length=30, unique=True)

    def __str__(self):
        return str(self.name)
    
    @staticmethod
    def list_keywords():
        return Keyword.objects.values_list('name', flat=True)

class Article(models.Model):
    """
    `QuestionViewSet` é uma viewset da `Question` model.
    provê criação de novas Perguntas e permite que o Player responda a uma pergunta.
    attributes: `author`, `published_date`, `title`, `subtitle`, `content`, `keyword_set`, 
                `created_at`, `article_type`, `status`
    methods: `publish`: Adiciona a data de publicação do artigo (Não está sendo utilizado)
             `exceeded_limit`: Verifica se o usuário já atingiu o limite de artigos
    """

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
    keyword_set = models.ManyToManyField(Keyword, verbose_name=_("Keyword"))
    title = models.CharField(verbose_name=_("Title"), max_length=200, default='', blank=False, null=False, unique=True)
    subtitle = models.CharField(verbose_name=_("Sub Title"), max_length=200, blank=True)
    content = models.TextField(verbose_name=_("Content"), max_length=2000, blank=True)
    created_date = models.DateTimeField(verbose_name=_("Created Date"), default=timezone.now, null=False)
    published_date = models.DateTimeField(verbose_name=_("Published Date"), blank=True, null=True)
    article_type = models.PositiveSmallIntegerField(choices=TYPE, verbose_name=_("Type"), default=0, null=False)
    status = models.PositiveSmallIntegerField(choices=STATUS, verbose_name=_("Status"), default=0, null=False)

    def __str__(self):
        if self.subtitle:
            return self.title + " - " + self.subtitle
        return self.title

    def publish(self):
        self.published_date = timezone.now()
        self.save()
    
    def exceeded_limit(self):
        return True if self.author.article_set.count() >= 50 else False
    
    def clean(self, *args, **kwargs):
        if self.exceeded_limit():
            raise ValidationError(_("Exceeded limit of articles per user"))
        super(Article, self).clean(*args, **kwargs)