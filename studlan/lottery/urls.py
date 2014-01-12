#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('studlan.lottery.views',
    # Main comp oversight
    url(r'^$', 'index', name='index'),
    url(r'^signup/(?P<lottery_id>\d+)/$', 'sign_up', name='sign_up'),
    url(r'^signoff/(?P<lottery_id>\d+)/$', 'sign_off', name='sign_off'),
)
