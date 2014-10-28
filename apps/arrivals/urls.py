# -*- coding: utf-8 -*-

from django.conf.urls import *

urlpatterns = patterns('apps.arrivals.views',
    url(r'^$', 'home', name='arrival_home'),
    url(r'^(?P<lan_id>\d+)/$', 'arrivals', name='arrivals'),
    url(r'^(?P<lan_id>\d+)/toggle/$', 'toggle', name='toggle'),
)
