#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url

urlpatterns = patterns('apps.seating.views',
    # Main comp oversight
    url(r'^$', 'main', name='seatings'),
    url(r'^(?P<lan_id>\d+)/$', 'main_filtered', name='seating_show_lan'),

    # Seating related
    url(r'^details/(?P<seating_id>\d+)/$', 'seating_details', name='seating_details'),
    url(r'^map/(?P<seating_id>\d+)/$', 'seating_map', name='map'),
    url(r'^details/(?P<seating_id>\d+)/join/(?P<seat_id>\d+)', 'join', name='take_seat'),
    url(r'^details/(?P<seating_id>\d+)/leave/(?P<seat_id>\d+)', 'leave', name='leave_seat'),

)
