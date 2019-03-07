# -*- coding: utf-8 -*-

from django.conf import settings
from django.contrib import admin

from apps.news.models import Article, ArticleTranslation


class ArticleTranslationInlineAdmin(admin.StackedInline):
    verbose_name = 'Translation'
    verbose_name_plural = 'Translations'
    model = ArticleTranslation
    max_num = len(settings.LANGUAGES)
    extra = 2


class ArticleAdmin(admin.ModelAdmin):
    inlines = [ArticleTranslationInlineAdmin]


admin.site.register(Article, ArticleAdmin)
