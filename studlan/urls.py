# -*- coding: utf-8 -*-

from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    
    url(r'^admin/', include(admin.site.urls)),

    url(r'^$', 'apps.news.views.main', name='root', kwargs={'page': 1}),
    url(r'^i18n/', include('django.conf.urls.i18n')),
    url(r'^login.html', 'apps.competition.views.log_in'),
    url(r'^logout.html', 'apps.competition.views.log_out'),
    url(r'^register.html', 'apps.competition.views.register_user'),
    url(r'^misc/remove_alert.html', 'apps.misc.views.remove_alert'),

    # app urls
    url(r'^api/',           include('apps.api.urls')),
    url(r'^arrivals/',      include('apps.arrivals.urls')),
    url(r'^auth/',          include('apps.authentication.urls')),
    url(r'^competition/',   include('apps.competition.urls')),
    url(r'^lan/',           include('apps.lan.urls')),
    url(r'^lottery/',       include('apps.lottery.urls')),
    url(r'^news/',          include('apps.news.urls')),
    url(r'^profile/',       include('apps.userprofile.urls')),
    url(r'^team/',          include('apps.team.urls')),
    url(r'^seating/',       include('apps.seating.urls')),
)

handler404 = 'apps.misc.views.handler404'
