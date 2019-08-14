
# -*- coding: utf-8 -*-

from django.conf.urls import url
from django.core.urlresolvers import reverse_lazy
from django.views.generic.base import RedirectView

from .views import close, details, draw, open_, sign_off, sign_up


list_ = RedirectView.as_view(url=reverse_lazy('competitions'), permanent=False)

urlpatterns = [
    url(r'^$', list_, name='lottery_list'),
    url(r'^(?P<lottery_id>\d+)/$', details, name='lottery_details'),
    url(r'^(?P<lottery_id>\d+)/signup/$', sign_up, name='lottery_sign_up'),
    url(r'^(?P<lottery_id>\d+)/signoff/$', sign_off, name='lottery_sign_off'),
    url(r'^(?P<lottery_id>\d+)/open/$', open_, name='lottery_open'),
    url(r'^(?P<lottery_id>\d+)/close/$', close, name='lottery_close'),
    url(r'^(?P<lottery_id>\d+)/draw/$', draw, name='lottery_draw'),
]
