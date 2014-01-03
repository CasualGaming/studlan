# -*- coding: utf-8 -*-

from django.conf.urls.defaults import *

urlpatterns = patterns('studlan.arrivals.views',
    url(r'^$', 'home', name='arrival_home'),
    url(r'^(?P<lan_id>\d+)/$', 'arrivals', name='arrivals'),
    url(r'^(?P<lan_id>\d+)/toggle_arrived/(?P<user_id>\d+)$', 'toggle_arrival', name='toggle_arrival'),
    url(r'^(?P<lan_id>\d+)/toggle_paid/(?P<user_id>\d+)$', 'toggle_paid', name='toggle_paid'),
    url(r'^(?P<lan_id>\d+)/toggle/$', 'toggle', name='toggle'),
)
