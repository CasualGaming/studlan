# -*- encoding: utf-8 -*-

from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('studlan.competition.views',
    url(r'^$', 'main', name='competitions'),
    url(r'^(?P<competition_id>\d+)/$', 'single', name='competition'),
    url(r'^(?P<competition_id>\d+)/join.html', 'join'),
    url(r'^(?P<competition_id>\d+)/leave.html', 'leave'),
    url(r'^(?P<competition_id>\d+)/forfeit.html', 'forfeit'),
)
