
# -*- coding: utf-8 -*-

from django.conf.urls import url

from .views import sendmail_send


urlpatterns = [
    url(r'^$', sendmail_send, name='sendmail_send'),
]
