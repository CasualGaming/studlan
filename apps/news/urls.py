# -*- coding: utf-8 -*-

from django.conf.urls import *

from apps.news.views import main, single, archive, faq, toParents

urlpatterns = [
    url(r'^$', main, name='news_main', kwargs={'page': 1}),
    url(r'^archive$', archive, name='archive', kwargs={'page': 1}),
    url(r'^faq', faq, name='faq'),
    url(r'^parents', toParents, name='to_parents'),
    url(r'^(?P<page>\d+)/$', main, name='news'),
    url(r'^item/(?P<article_id>\d+)/$', single, name='news_single'),
]
