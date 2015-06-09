#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url

urlpatterns = patterns('apps.seating.views',
    # Main comp oversight
    url(r'^$', 'main', name='seatings'),
    url(r'^(?P<lan_id>\d+)/(?P<seating_id>\d+)/$', 'seating_details', name='seating_details'),
    url(r'^(?P<lan_id>\d+)/$', 'seating_details', name='seating_details'),

    # Seating related
    url(r'^map/(?P<seating_id>\d+)/$', 'seating_map', name='map'),
    url(r'^list/(?P<seating_id>\d+)/$', 'seating_list', name='list'),

    url(r'^(?P<seating_id>\d+)/(?P<seat_id>\d+)/take/$', 'take', name='take_seat'),
    url(r'^(?P<lan_id>\d+)/(?P<seating_id>\d+)/(?P<seat_id>\d+)/take/$', 'take2', name='take_seat'),

    url(r'^(?P<seating_id>\d+)/(?P<seat_id>\d+)/leave/$', 'leave', name='leave_seat'),
    url(r'^(?P<lan_id>\d+)/(?P<seating_id>\d+)/(?P<seat_id>\d+)/leave/$', 'leave2', name='leave_seat'),
)
