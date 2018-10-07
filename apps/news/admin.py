# -*- coding: utf-8 -*-

from django.conf import settings
from django.contrib import admin

from apps.news.models import Article, ArticleTranslation, FAQ, FAQTranslation, ToParents, ToParentsTranslation

class ArticleTranslationInlineAdmin(admin.StackedInline):
    verbose_name = "Translation"
    verbose_name_plural = "Translations"
    model = ArticleTranslation
    max_num = len(settings.LANGUAGES)
    extra = 2

class ArticleAdmin(admin.ModelAdmin):
    inlines = [ArticleTranslationInlineAdmin]

class FAQTranslationInlineAdmin(admin.StackedInline):
    verbose_name = "Translation"
    verbose_name_plural = "Translations"
    model = FAQTranslation
    max_num = len(settings.LANGUAGES)
    extra = 2

class FAQAdmin(admin.ModelAdmin):
    inlines = [FAQTranslationInlineAdmin]

class ToParentsTranslationInlineAdmin(admin.StackedInline):
    verbose_name = "Translation"
    verbose_name_plural = "Translations"
    model = ToParentsTranslation
    max_num = len(settings.LANGUAGES)
    extra = 2

class ToParentsAdmin(admin.ModelAdmin):
    inlines = [ToParentsTranslationInlineAdmin,]


admin.site.register(Article, ArticleAdmin)
admin.site.register(FAQ, FAQAdmin)
admin.site.register(ToParents, ToParentsAdmin)
