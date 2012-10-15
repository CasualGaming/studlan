#!/usr/bin/python
# -*- coding: utf-8 -*-
import datetime

from django.db import models


class Article(models.Model):

    title = models.CharField('title', max_length=50)
    body = models.TextField('body')
    pub_date = models.DateTimeField('published', default=datetime.datetime.now)

    def count(self):
        return len(Article.objects.all())

    @models.permalink
    def get_absolute_url(self):
        return ('news_single', (), {'article_id': self.id})

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ['-pub_date']
