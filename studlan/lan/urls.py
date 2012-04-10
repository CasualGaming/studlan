# -*- coding: utf-8 -*-

from django.conf.urls.defaults import *

urlpatterns = patterns('studlan.lan.views',
    url(r'^$', 'list', name='lan_list'),
    url(r'^(?P<lan_id>\d+)/$', 'details', name='lan_details'),
    url(r'^(?P<lan_id>\d+)/(?P<user_id>\d+)$', 'history', name='lan_history'),
)
