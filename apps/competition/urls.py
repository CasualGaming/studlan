# -*- coding: utf-8 -*-

from django.conf.urls import url

from .views import (activity_details, activity_details_filtered, competition_details, forfeit, join,
                    lan_compos, lan_list, leave, main, register_score, schedule, schedule_details, schedule_lan_list, start_compo, submit_score)


urlpatterns = [
    # Main comp oversight
    url(r'^$', main, name='competitions'),
    url(r'^list/$', lan_list, name='competitions_lan_list'),
    url(r'^(?P<lan_id>\d+)/$', lan_compos, name='competitions_lan_compos'),

    # Competition related
    url(r'^compo/(?P<competition_id>\d+)/$', competition_details, name='competition_details'),
    url(r'^compo/(?P<competition_id>\d+)/join/', join, name='join_comp'),
    url(r'^compo/(?P<competition_id>\d+)/leave/', leave, name='leave_comp'),
    url(r'^compo/(?P<competition_id>\d+)/forfeit/', forfeit, name='forfeit_comp'),
    url(r'^compo/(?P<competition_id>\d+)/(?P<match_id>\d+)/submit_score/', submit_score, name='submit_score'),
    url(r'^compo/(?P<competition_id>\d+)/(?P<match_id>\d+)/(?P<player_id>\d+)/register_score/', register_score, name='register_score'),
    url(r'^compo/(?P<competition_id>\d+)/start_compo/', start_compo, name='start_compo'),

    # Activiy related
    url(r'^activity/(?P<activity_id>\d+)/$', activity_details, name='activity_details'),
    url(r'^(?P<lan_id>\d+)/activity/(?P<activity_id>\d+)/$', activity_details_filtered, name='activity_details_show_lan'),

    # Schedule related
    url(r'^schedule/$', schedule, name='schedule'),
    url(r'^schedule/list/$', schedule_lan_list, name='schedule_lan_list'),
    url(r'^schedule/(?P<lan_id>\d+)/$', schedule_details, name='schedule_details'),
]
