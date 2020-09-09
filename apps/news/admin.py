# -*- coding: utf-8 -*-

from django.conf import settings
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from apps.news.models import Article, ArticleTranslation


class ArticleTranslationInlineAdmin(admin.StackedInline):
    verbose_name = _(u'Translation')
    verbose_name_plural = _(u'Translations')
    model = ArticleTranslation
    max_num = len(settings.LANGUAGES)
    extra = 2


class ArticleAdmin(admin.ModelAdmin):
    inlines = [ArticleTranslationInlineAdmin]
    list_display = ['__unicode__', 'pub_date']
    list_filter = ['relevant_to']


admin.site.register(Article, ArticleAdmin)
