# -*- coding: utf-8 -*-

from django.conf import settings
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from apps.news.models import Article


class ArticleAdmin(admin.ModelAdmin):
    list_display = ['pub_date']
    list_filter = ['relevant_to']


admin.site.register(Article, ArticleAdmin)
