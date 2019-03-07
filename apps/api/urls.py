# -*- coding: utf-8 -*-

from django.conf.urls import url

from .views import change_arrived, change_paid

urlpatterns = [
    url(r'(?P<api_key>\w+)/arrived/(?P<lan_id>\d+)/(?P<username>\w+)/(?P<status>\d)/$', change_arrived, name='api_change_arrived'),
    url(r'(?P<api_key>\w+)/paid/(?P<lan_id>\d+)/(?P<username>\w+)/(?P<status>\d)/$', change_paid, name='api_change_paid'),
]
