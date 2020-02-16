# -*- coding: utf-8 -*-

from django.conf.urls import url

from apps.news.views import archive, main, single

urlpatterns = [
    url(r'^$', main, name='news_main', kwargs={'page': 1}),
    url(r'^(?P<page>\d+)/$', main, name='news'),
    url(r'^archive/$', archive, name='archive_main', kwargs={'page': 1}),
    url(r'^archive/(?P<page>\d+)$', archive, name='archive'),
    url(r'^item/(?P<article_id>\d+)/$', single, name='news_single'),
]
