# -*- encoding: utf-8 -*-

from django.conf.urls.defaults import patterns, url
from studlan.news.views import main

urlpatterns = patterns('studlan.news.views', url(r'^$', 'main', name='news'))
