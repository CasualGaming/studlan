# -*- coding: utf-8 -*-

from django.conf import settings
from django.conf.urls import include, re_path
from django.contrib import admin
from django.views.generic.base import RedirectView

from apps.lan import views as lan_view
from apps.lan.models import LAN
from apps.misc import views as misc_view
from apps.sponsor import views as sponsor_view

urlpatterns = [
#     # Django
    re_path(r'^admin/', admin.site.urls),
    re_path(r'^i18n/', include('django.conf.urls.i18n')),

    # Apps
    re_path(r'^api/', include('apps.api.urls')),
    re_path(r'^arrivals/', include('apps.arrivals.urls')),
    re_path(r'^auth/', include('apps.authentication.urls')),
    re_path(r'^competition/', include('apps.competition.urls')),
    re_path(r'^lan/', include('apps.lan.urls')),
    re_path(r'^lottery/', include('apps.lottery.urls')),
    re_path(r'^news/', include('apps.news.urls')),
    re_path(r'^payment/', include('apps.payment.urls')),
    re_path(r'^poll/', include('apps.poll.urls')),
    re_path(r'^profile/', include('apps.userprofile.urls')),
    re_path(r'^team/', include('apps.team.urls')),
    re_path(r'^seating/', include('apps.seating.urls')),
    re_path(r'^sendmail/', include('apps.sendmail.urls')),
    re_path(r'^statistics/', include('apps.statistics.urls')),
    re_path(r'^messages/', include('postman.urls', namespace='postman')),

    # Views
    re_path(r'^$', RedirectView.as_view(url='/lan', permanent=False), name='root'),
    re_path(r'^misc/remove_alert.html$', misc_view.remove_alert),
    re_path(r'^misc/change_language$', misc_view.change_language),
    re_path(r'^sponsors/', sponsor_view.index, name='sponsors'),

    # LAN slug (lowest priority)
    re_path(r'^(?P<lan_slug>' + LAN.SLUG_REGEX + r')/$', lan_view.details_slug, name='lan_details_slug'),
]

if settings.DEBUG:
    urlpatterns += [
        re_path(r'^404$', misc_view.handler404, name='404_handler'),
        re_path(r'^500$', misc_view.handler500, name='500_handler'),
    ]

handler404 = 'apps.misc.views.handler404'
handler500 = 'apps.misc.views.handler500'
