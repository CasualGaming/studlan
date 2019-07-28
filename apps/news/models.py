# -*- coding: utf-8 -*-
from datetime import datetime

from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _lazy

from translatable.models import TranslatableModel, get_translation_model

from apps.lan.models import LAN


class Article(TranslatableModel):
    pub_date = models.DateTimeField(_lazy(u'date published'), default=datetime.now)
    relevant_to = models.ManyToManyField(LAN, verbose_name=_lazy(u'relevant LANs'), blank=True)
    pinned = models.BooleanField(_lazy(u'pinned'), default=False, help_text=_lazy(u'Pinned articles are shown before non-pinned ones.'))

    def count(self):
        return len(Article.objects.all())

    def get_absolute_url(self):
        return reverse('news_single', kwargs={'article_id': self.id})

    class Meta:
        verbose_name = _lazy(u'news article')
        verbose_name_plural = _lazy(u'news articles')
        ordering = ['-pub_date']


class ArticleTranslation(get_translation_model(Article, 'Article')):
    translated_title = models.CharField(_lazy(u'title'), max_length=50)
    translated_body = models.TextField(_lazy(u'content'))

    def __unicode__(self):
        return self.translated_title

    class Meta:
        verbose_name = _lazy(u'news article translation')
        verbose_name_plural = _lazy(u'news article translations')
