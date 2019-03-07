# -*- coding: utf-8 -*-

from datetime import datetime

from django import template

from apps.lan.models import LAN
from apps.sponsor.models import SponsorRelation


register = template.Library()


@register.inclusion_tag('sponsor/sponsor_list.html')
def show_sponsor_list():

    lans = LAN.objects.filter(end_date__gte=datetime.now())
    if lans:
        sponsor_relations = SponsorRelation.objects.filter(lan__in=lans)
    else:
        sponsor_relations = []

    sponsors = [sponsor_relation.sponsor for sponsor_relation in sponsor_relations]

    return {'sponsors': sponsors}
