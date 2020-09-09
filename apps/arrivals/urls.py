# -*- coding: utf-8 -*-

from django.conf.urls import url

from .views import arrivals, home, toggle

urlpatterns = [
    url(r'^$', home, name='arrival_home'),
    url(r'^(?P<lan_id>\d+)/$', arrivals, name='arrivals'),
    url(r'^(?P<lan_id>\d+)/toggle/$', toggle, name='toggle'),
]
