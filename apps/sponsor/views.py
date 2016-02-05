#!/usr/bin/python
# -*- coding: utf-8 -*-

from datetime import datetime

from django.shortcuts import render

from apps.sponsor.models import Sponsor, SponsorRelation
from apps.lan.models import LAN


def index(request):
    
    lans = LAN.objects.filter(end_date__gte=datetime.now())
    if lans:
        sponsor_relations = SponsorRelation.objects.filter(lan__in=lans)
    else:
        sponsor_relations = []

    active_sponsors = [sponsor_relation.sponsor for sponsor_relation in sponsor_relations]

    sponsors = list(Sponsor.objects.all())

    for sponsor in sponsors:
        if not sponsor.banner:
            sponsor.banner = 'http://placehold.it/300x150'

    inactive_sponsors = [sponsor for sponsor in sponsors if sponsor not in active_sponsors]

    return render(request, 'sponsor/sponsors.html', 
        {'active_sponsors': active_sponsors, 'inactive_sponsors': inactive_sponsors})