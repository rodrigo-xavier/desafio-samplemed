from django.contrib import admin
from blog import models
from reversion.admin import VersionAdmin

@admin.register(models.User)
class UserAdmin(VersionAdmin):
    pass

@admin.register(models.Article)
class ArticleAdmin(VersionAdmin):
    pass