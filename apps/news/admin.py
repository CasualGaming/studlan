# -*- coding: utf-8 -*-

from django.conf import settings
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _lazy

from apps.news.models import Article, ArticleTranslation


class ArticleTranslationInlineAdmin(admin.StackedInline):
    verbose_name = _lazy(u'Translation')
    verbose_name_plural = _lazy(u'Translations')
    model = ArticleTranslation
    max_num = len(settings.LANGUAGES)
    extra = 2


class ArticleAdmin(admin.ModelAdmin):
    inlines = [ArticleTranslationInlineAdmin]


admin.site.register(Article, ArticleAdmin)
