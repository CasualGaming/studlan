# -*- coding: utf-8 -*-

from django.conf.urls import url

from .views import home, listing, details, attend, unattend, list_paid

urlpatterns = [
    url(r'^$', home, name='lan_home'),
    url(r'^list/$', listing, name='lan_listing'),
    url(r'^(?P<lan_id>\d+)/$', details, name='lan_details'),
    url(r'^(?P<lan_id>\d+)/attend/$', attend, name='lan_attend'),
    url(r'^(?P<lan_id>\d+)/unattend/$', unattend, name='lan_unattend'),
    url(r'^(?P<lan_id>\d+)/list_paid/$', list_paid, name='lan_list_paid'),
]
