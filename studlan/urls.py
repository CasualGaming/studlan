# -*- coding: utf-8 -*-

from django.conf.urls import include, url
from django.contrib import admin
from apps.news import views as news_view
from apps.misc import views as misc_view
from apps.sponsor import views as sponsor_view
from apps.payment import views as payment_view

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^i18n/', include('django.conf.urls.i18n')),

    url(r'^$', news_view.main, name='root', kwargs={'page': 1}),
    url(r'^misc/remove_alert.html$', misc_view.remove_alert),
    url(r'^misc/change_language$', misc_view.change_language),
    url(r'^sponsors/', sponsor_view.index, name='sponsors'),
    url(r'^payment/(?P<ticket_id>\d+)/$', payment_view.payment, name='payment'),

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
    url(r'^messages/',      include('postman.urls', namespace='postman')),
]

handler404 = 'apps.misc.views.handler404'
