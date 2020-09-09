
# -*- coding: utf-8 -*-

from django.conf.urls import url
from django.core.urlresolvers import reverse_lazy
from django.views.generic.base import RedirectView

from .views import close, details, open_, unvote, vote


list_ = RedirectView.as_view(url=reverse_lazy('competitions'), permanent=False)

urlpatterns = [
    url(r'^$', list_, name='poll_list'),
    url(r'^(?P<poll_id>\d+)/$', details, name='poll_details'),
    url(r'^(?P<poll_id>\d+)/vote/(?P<option_id>\d+)/$', vote, name='poll_vote'),
    url(r'^(?P<poll_id>\d+)/unvote/$', unvote, name='poll_unvote'),
    url(r'^(?P<poll_id>\d+)/open/$', open_, name='poll_open'),
    url(r'^(?P<poll_id>\d+)/close/$', close, name='poll_close'),
]
