#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('studlan.lottery.views',
    # Main comp oversight
    url(r'^$', 'main', name='lottery'),
    url(r'^signup/$', 'signup', name='signup'),
)
