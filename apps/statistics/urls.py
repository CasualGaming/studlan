# -*- coding: utf-8 -*-

from django.conf.urls import url

from .views import statistics, statistics_list

urlpatterns = [
    url(r'^$', statistics_list, name='statistics_list'),
    url(r'^(?P<lan_id>\d+)/$', statistics, name='statistics'),
]
