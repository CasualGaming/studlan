from django.conf.urls.defaults import *

urlpatterns = patterns('studlan.team.views',
    url(r'^$', 'teams', name='teams'),
    url(r'^create/$', 'create_team', name='create_team'),
    url(r'^(?P<team_tag>\w+)/$', 'team', name='team'),
    url(r'^(?P<team_id>\w+)/disband/$', 'disband_team', name='disband_team'),
    url(r'^(?P<team_tag>\w+)/add/$', 'add_member', name='add_member'),
    url(r'^(?P<team_tag>\w+)/remove/(?P<user_id>\d+)/$', 'remove_member', name='remove_member'),
)
