#!/usr/bin/python
# -*- coding: utf-8 -*-
import datetime

from django.db import models
from translatable.models import TranslatableModel, get_translation_model


class Article(TranslatableModel):

    pub_date = models.DateTimeField('published', default=datetime.datetime.now)

    def count(self):
        return len(Article.objects.all())

    @models.permalink
    def get_absolute_url(self):
        return ('news_single', (), {'article_id': self.id})

    class Meta:
        ordering = ['-pub_date']

class ArticleTranslation(get_translation_model(Article, "Article")):
    translated_title = models.CharField('title', max_length=50)
    translated_body = models.TextField('body')
    
    def __unicode__(self):
        return self.title
