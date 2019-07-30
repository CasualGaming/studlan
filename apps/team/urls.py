# -*- coding: utf-8 -*-

from django.conf.urls import url

from .views import accept_member_invite, create_team, decline_member_invite, disband_team, invite_member, kick_member, leave_team, my_teams, show_team, teams, uninvite_member


urlpatterns = [
    url(r'^$', teams, name='teams'),
    url(r'^mine/$', my_teams, name='my_teams'),
    url(r'^create/$', create_team, name='create_team'),
    url(r'^(?P<team_id>\d+)/$', show_team, name='show_team'),
    url(r'^(?P<team_id>\d+)/disband/$', disband_team, name='disband_team'),
    url(r'^(?P<team_id>\d+)/invite_member/$', invite_member, name='invite_member'),
    url(r'^(?P<team_id>\d+)/uninvite_member/$', uninvite_member, name='uninvite_member'),
    url(r'^(?P<team_id>\d+)/accept_invite/$', accept_member_invite, name='accept_member_invite'),
    url(r'^(?P<team_id>\d+)/decline_invite/$', decline_member_invite, name='decline_member_invite'),
    url(r'^(?P<team_id>\d+)/leave/$', leave_team, name='leave_team'),
    url(r'^(?P<team_id>\d+)/kick_member/$', kick_member, name='kick_member'),
]
