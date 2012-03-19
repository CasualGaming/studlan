from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'studlan.news.views.main', name='root'),
    url(r'^login.html', 'studlan.competition.views.log_in'),
    url(r'^logout.html', 'studlan.competition.views.log_out'),
    url(r'^register.html', 'studlan.competition.views.register_user'),
    url(r'^competitions/', include('studlan.competition.urls')),
    url(r'^misc/remove_alert.html', 'studlan.misc.views.remove_alert'),
    url(r'^teams/$', 'studlan.competition.views.teams', name='teams'),
    url(r'^team/(?P<team_tag>\w+)$', 'studlan.competition.views.team', name='team'),
    url(r'^team/(?P<team_tag>\w+)/add_member.html', 'studlan.competition.views.add_member'),
    url(r'^team/(?P<team_tag>\w+)/remove/(?P<member_id>\d+)$', 'studlan.competition.views.remove_member'),
    url(r'^teams/create_team.html', 'studlan.competition.views.create_team'),
    url(r'^arrivals/$', 'studlan.misc.views.arrivals', name='arrivals'),
    url(r'^arrivals/toggle/(?P<user_id>\d+)$', 'studlan.misc.views.toggle_arrival', name='toggle_arrival'),

    # app urls
    url(r'^auth/',      include('studlan.auth.urls')),
    url(r'^profile/',   include('studlan.userprofile.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)

handler404 = 'studlan.misc.views.handler404'
