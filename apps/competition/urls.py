#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.conf.urls import url
from .views import main, main_filtered, competition_details, join, leave, forfeit, activity_details, activity_details_filtered, schedule

urlpatterns = [
    # Main comp oversight
    url(r'^$', main, name='competitions'),
    url(r'^(?P<lan_id>\d+)/$', main_filtered, name='competitions_show_lan'),

    # Competition related
    url(r'^compo/(?P<competition_id>\d+)/$', competition_details, name='competition_details'),
    url(r'^compo/(?P<competition_id>\d+)/join/', join, name='join_comp'),
    url(r'^compy/(?P<competition_id>\d+)/leave/', leave, name='leave_comp'),
    url(r'^compo/(?P<competition_id>\d+)/forfeit/', forfeit, name='forfeit_comp'),

    # Activiy related
    url(r'^activity/(?P<activity_id>\d+)/$', activity_details, name='activity_details'),
    url(r'^(?P<lan_id>\d+)/activity/(?P<activity_id>\d+)/$', activity_details_filtered, name='activity_details_show_lan'),

    # Schedule related
    url(r'^schedule/', schedule, name='competition_schedule')
]
