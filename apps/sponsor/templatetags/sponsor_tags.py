# -*- coding: utf-8 -*-

from datetime import datetime

from django import template

from apps.lan.models import LAN
from apps.sponsor.models import SponsorRelation


register = template.Library()


@register.assignment_tag
def upcoming_lan_sponsors():
    lans = LAN.objects.filter(end_date__gte=datetime.now())
    if lans:
        sponsor_relations = SponsorRelation.objects.filter(lan__in=lans).select_related('sponsor').order_by('-priority')
        return [r.sponsor for r in sponsor_relations]
    else:
        return None
