# -*- encoding: utf-8 -*-

from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('studlan.competition.views',
    url(r'^$', 'main', name='competitions'),
    url(r'^(?P<competition_id>\d+)/$', 'single', name='competition')
)
