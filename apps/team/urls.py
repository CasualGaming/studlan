# -*- coding: utf-8 -*-

from django.conf.urls import *

urlpatterns = patterns('apps.team.views',
    url(r'^$', 'teams', name='teams'),
    url(r'^mine/$', 'my_teams', name='my_teams'),
    url(r'^create/$', 'create_team', name='create_team'),
    url(r'^(?P<team_id>\d+)/disband/$', 'disband_team', name='disband_team'),
    url(r'^(?P<team_id>\d+)/add/$', 'add_member', name='add_member'),
    url(r'^(?P<team_id>\d+)/invite/$', 'invite_member', name='invite_member'),
    url(r'^(?P<team_id>\d+)/join/$', 'join_team', name='join_team'),
    url(r'^(?P<team_id>\d+)/remove/(?P<user_id>\d+)/$', 'remove_member', name='remove_member'),
    url(r'^(?P<team_id>\d+)/$', 'show_team', name='show_team'),
)
