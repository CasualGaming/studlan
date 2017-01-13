#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url

urlpatterns = patterns('apps.competition.views',
    # Main comp oversight
    url(r'^$', 'main', name='competitions'),
    url(r'^(?P<lan_id>\d+)/$', 'main_filtered', name='competitions_show_lan'),

    # Competition related
    url(r'^compo/(?P<competition_id>\d+)/$', 'competition_details', name='competition_details'),
    url(r'^compo/(?P<competition_id>\d+)/join/', 'join', name='join_comp'),
    url(r'^compo/(?P<competition_id>\d+)/(?P<match_id>\d+)/submit_score/', 'submit_score', name='submit_score'),
    url(r'^compo/(?P<competition_id>\d+)/(?P<match_id>\d+)/(?P<player_id>\d+)/register_score/', 'register_score', name='register_score'),
    url(r'^compo/(?P<competition_id>\d+)/start_compo/', 'start_compo', name='start_compo'),
    url(r'^compy/(?P<competition_id>\d+)/leave/', 'leave', name='leave_comp'),
    url(r'^compo/(?P<competition_id>\d+)/forfeit/', 'forfeit', name='forfeit_comp'),

    # Activiy related
    url(r'^activity/(?P<activity_id>\d+)/$', 'activity_details', name='activity_details'),
    url(r'^(?P<lan_id>\d+)/activity/(?P<activity_id>\d+)/$', 'activity_details_filtered', name='activity_details_show_lan'),
)
