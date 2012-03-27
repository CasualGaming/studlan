#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('studlan.competition.views',
    # Main comp oversight
    url(r'^$', 'main', name='competitions'),

    # Competition related
    url(r'^(?P<competition_id>\d+)/$', 'competition_details', name='competition_details'),
    url(r'^(?P<competition_id>\d+)/join/', 'join', name='join_comp'),
    url(r'^(?P<competition_id>\d+)/leave/', 'leave', name='leave_comp'),
    url(r'^(?P<competition_id>\d+)/forfeit/', 'forfeit', name='forfeit_comp'),

    # Activiy related
    url(r'^activity/(?P<activity_id>\d+)/$', 'activity_details', name='activity_details'),
)
