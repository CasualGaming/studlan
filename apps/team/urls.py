# -*- coding: utf-8 -*-

from django.conf.urls import url
from .views import teams, my_teams, create_team, disband_team, add_member, invite_member, remove_invitation, join_team, remove_member, show_team

urlpatterns = [
    url(r'^$', teams, name='teams'),
    url(r'^mine/$', my_teams, name='my_teams'),
    url(r'^create/$', create_team, name='create_team'),
    url(r'^(?P<team_id>\d+)/disband/$', disband_team, name='disband_team'),
    url(r'^(?P<team_id>\d+)/add/$', add_member, name='add_member'),
    url(r'^(?P<team_id>\d+)/invite/$', invite_member, name='invite_member'),
    url(r'^(?P<team_id>\d+)/remove_invitation/(?P<invitation_token>[\w-]+)/$', remove_invitation, name='remove_invitation'),
    url(r'^(?P<team_id>\d+)/join/$', join_team, name='join_team'),
    url(r'^(?P<team_id>\d+)/remove/(?P<user_id>\d+)/$', remove_member, name='remove_member'),
    url(r'^(?P<team_id>\d+)/$', show_team, name='show_team'),
]
