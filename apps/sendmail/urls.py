
# -*- coding: utf-8 -*-

from django.conf.urls import url

from .views import sendmail_list, sendmail_send, sendmail_view


urlpatterns = [
    url(r'^$', sendmail_list, name='sendmail_list'),
    url(r'^view/(?P<mail_uuid>[^/]+)/$', sendmail_view, name='sendmail_view'),
    url(r'^send/$', sendmail_send, name='sendmail_send'),
]
