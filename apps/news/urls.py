# -*- coding: utf-8 -*-

from django.conf.urls import *

from apps.news.views import main, single

urlpatterns = [
    url(r'^$', main, name='news_main', kwargs={'page': 1}),
    url(r'^(?P<page>\d+)/$', main, name='news'),
    url(r'^item/(?P<article_id>\d+)/$', single, name='news_single'),
]
