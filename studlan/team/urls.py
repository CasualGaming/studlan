from django.conf.urls.defaults import *

urlpatterns = patterns('studlan.team.views',
    url(r'^$', 'teams', name='teams'),
    url(r'^create/$', 'create_team', name='create_team'),
    url(r'^(?P<team_tag>\w+)/$', 'team', name='team'),
    url(r'^(?P<team_tag>\w+)/add/$', 'add_member'),
    url(r'^(?P<team_tag>\w+)/remove/(?P<user_id>\d+)/$', 'remove_member'),
)
