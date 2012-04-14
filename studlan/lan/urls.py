# -*- coding: utf-8 -*-

from django.conf.urls.defaults import *

urlpatterns = patterns('studlan.lan.views',
    url(r'^$', 'home', name='lan_home'),
    url(r'^list/$', 'listing', name='lan_listing'),
    url(r'^(?P<lan_id>\d+)/$', 'details', name='lan_details'),
    url(r'^(?P<lan_id>\d+)/attend/$', 'attend', name='lan_attend'),
    url(r'^(?P<lan_id>\d+)/unattend/$', 'unattend', name='lan_unattend'),
    url(r'^(?P<lan_id>\d+)/(?P<user_id>\d+)$', 'history', name='lan_history'),
)
