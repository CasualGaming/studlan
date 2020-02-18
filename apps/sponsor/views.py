# -*- coding: utf-8 -*-

from django.db.models import Count
from django.shortcuts import render

from apps.lan.models import LAN


def index(request):
    lans = LAN.objects.annotate(sponsor_count=Count('sponsorrelation')).filter(sponsor_count__gt=0).prefetch_related('sponsorrelation_set__sponsor').order_by('-start_date')
    return render(request, 'sponsor/sponsors.html', {'lans': lans, 'hide_sidebar': True})
