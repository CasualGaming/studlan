#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url

urlpatterns = patterns('apps.lottery.views',
    # Main comp oversight
    url(r'^$', 'index', name='lottery'),
    url(r'^signup/(?P<lottery_id>\d+)/$', 'sign_up', name='sign_up'),
    url(r'^signoff/(?P<lottery_id>\d+)/$', 'sign_off', name='sign_off'),
    url(r'^drawing/$', 'drawing', name='drawing'),
    url(r'^drawing/(?P<lottery_id>\d+)/$', 'drawing', name='drawing'),
    url(r'^draw/(?P<lottery_id>\d+)/$', 'draw', name='draw'),
)
