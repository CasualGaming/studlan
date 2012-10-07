# -*- coding: utf-8 -*-

from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    ## These urls should not take the lan parameter
    url(r'^$', 'studlan.lan.views.dispatch', name='root'),
    url(r'^login.html', 'studlan.competition.views.log_in'),
    url(r'^logout.html', 'studlan.competition.views.log_out'),
    url(r'^register.html', 'studlan.competition.views.register_user'),
    url(r'^misc/remove_alert.html', 'studlan.misc.views.remove_alert'),

    url(r'^auth/',          include('studlan.authentication.urls')),
    url(r'^profile/',       include('studlan.userprofile.urls')),
    url(r'^team/',          include('studlan.team.urls')),

    # These apps are bound by the parameter, but they do not need to accept it
    # in their views
    url(r'^[\w\d]{1,7}/', 'studlan.news.views.main', name='front_page', kwargs={'page': 1}), 
    url(r'^(?P<lan_slug>[\w\d]{1,7})/arrivals/',        include('studlan.arrivals.urls')),
    url(r'^(?P<lan_slug>[\w\d]{1,7})/competition/',     include('studlan.competition.urls')),
    url(r'^(?P<lan_slug>[\w\d]{1,7})/lan/',             include('studlan.lan.urls')),
    url(r'^[\w\d]{1,7}/news/',                          include('studlan.news.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)

handler404 = 'studlan.misc.views.handler404'
