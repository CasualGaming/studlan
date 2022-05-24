
# -*- coding: utf-8 -*-

from django.conf.urls import url

from .views import sendmail_list, sendmail_send


urlpatterns = [
    url(r'^$', sendmail_list, name='sendmail_list'),
    url(r'^send/$', sendmail_send, name='sendmail_send'),
]
