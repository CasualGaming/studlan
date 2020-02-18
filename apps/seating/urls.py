# -*- coding: utf-8 -*-

from django.conf.urls import url

from .views import lan_list, leave_seat, main, seating_details, seating_list, seating_map, take_seat


urlpatterns = [
    url(r'^$', main, name='seatings'),
    url(r'^list/$', lan_list, name='seating_lan_list'),
    url(r'^(?P<lan_id>\d+)/$', seating_details, name='seating_details'),
    url(r'^(?P<lan_id>\d+)/(?P<seating_id>\d+)/$', seating_details, name='seating_details'),
    url(r'^(?P<lan_id>\d+)/(?P<seating_id>\d+)/(?P<seat_id>\d+)/$', seating_details, name='seating_details'),
    url(r'^(?P<seating_id>\d+)/take_seat/$', take_seat, name='take_seat'),
    url(r'^(?P<seating_id>\d+)/leave_seat/$', leave_seat, name='leave_seat'),
    url(r'^(?P<seating_id>\d+)/map/$', seating_map, name='seating_map'),
    url(r'^(?P<seating_id>\d+)/list/$', seating_list, name='seating_list'),
]
