# -*- coding: utf-8 -*-

from django.conf.urls import url

from .views import make_payment, payment, payment_info, payment_info_static

urlpatterns = [
    url(r'^info/(?P<ticket_type_id>\d+)/$', payment_info, name='payment_info'),
    url(r'^info/$', payment_info_static, name='payment_info_static'),
    url(r'^(?P<ticket_type_id>\d+)/$', payment, name='payment'),
    url(r'^(?P<ticket_type_id>\d+)/pay$', make_payment, name='make_payment'),
]
