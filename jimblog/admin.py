from django.contrib import admin
from .models import Article, ArticleColumn

# Register your models here.


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created', 'updated', 'column')


admin.site.register(Article, ArticleAdmin)
admin.site.register(ArticleColumn)
