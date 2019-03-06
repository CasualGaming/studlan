# -*- coding: utf-8 -*-

from django.conf.urls import url

from .views import main, seating_details, seating_map, seating_list, take, take2, leave, leave2


urlpatterns = [
    # Main comp oversight
    url(r'^$', main, name='seatings'),
    url(r'^(?P<lan_id>\d+)/(?P<seating_id>\d+)/$', seating_details, name='seating_details'),
    url(r'^(?P<lan_id>\d+)/(?P<seating_id>\d+)/(?P<seat_id>\d+)/$', seating_details, name='seating_details'),
    url(r'^(?P<lan_id>\d+)/$', seating_details, name='seating_details'),

    # Seating related
    url(r'^map/(?P<seating_id>\d+)/$', seating_map, name='map'),
    url(r'^list/(?P<seating_id>\d+)/$', seating_list, name='list'),

    url(r'^(?P<seating_id>\d+)/(?P<seat_id>\d+)/take/$', take, name='take_seat'),
    url(r'^(?P<lan_id>\d+)/(?P<seating_id>\d+)/(?P<seat_id>\d+)/take/$', take2, name='take_seat'),

    url(r'^(?P<seating_id>\d+)/(?P<seat_id>\d+)/leave/$', leave, name='leave_seat'),
    url(r'^(?P<lan_id>\d+)/(?P<seating_id>\d+)/(?P<seat_id>\d+)/leave/$', leave2, name='leave_seat'),
]
