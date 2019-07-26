# -*- coding: utf-8 -*-

from django.conf.urls import url

from .views import add_alias, alias, history, my_profile, remove_alias, update_profile, user_competitions, user_inbox, user_profile


urlpatterns = [
    url(r'^$', my_profile, name='my_profile'),
    url(r'^update/$', update_profile, name='update_profile'),
    url(r'^competitions/$', user_competitions, name='user_competitions'),
    url(r'^history/$', history, name='user_history'),
    url(r'^inbox/$', user_inbox, name='inbox'),
    url(r'^alias/$', alias, name='alias'),
    url(r'^alias/add', add_alias, name='add_alias'),
    url(r'^alias/(?P<alias_id>\d+)/remove/$', remove_alias, name='remove_alias'),
    url(r'^(?P<username>[\w-]+)/$', user_profile, name='public_profile'),
]
