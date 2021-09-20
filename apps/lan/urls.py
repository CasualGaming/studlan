# -*- coding: utf-8 -*-

from django.conf.urls import url

from .views import attend, details_id, home, list_paid, listing, ticket_list, ticket_list_home, ticket_list_lan_list, unattend

urlpatterns = [
    url(r'^$', home, name='lan_home'),
    url(r'^list/$', listing, name='lan_listing'),
    url(r'^tickets/$', ticket_list_home, name='lan_tickets_home'),
    url(r'^tickets/list/$', ticket_list_lan_list, name='lan_tickets_lan_list'),
    url(r'^(?P<lan_id>\d+)/$', details_id, name='lan_details'),
    url(r'^(?P<lan_id>\d+)/tickets/$', ticket_list, name='lan_tickets'),
    url(r'^(?P<lan_id>\d+)/attend/$', attend, name='lan_attend'),
    url(r'^(?P<lan_id>\d+)/unattend/$', unattend, name='lan_unattend'),
    url(r'^(?P<lan_id>\d+)/list_paid/$', list_paid, name='lan_list_paid'),
]
