# -*- coding: utf-8 -*-

from datetime import datetime

from django import template

from apps.sponsor.models import SponsorRelation


register = template.Library()


@register.assignment_tag
def upcoming_lan_sponsors():
    relations = SponsorRelation.objects.filter(lan__end_date__gte=datetime.now()).select_related('sponsor').order_by('-priority')
    sponsors = []
    # Map and remove lower-priority duplicates
    for relation in relations:
        if relation.sponsor not in sponsors:
            sponsors.append(relation.sponsor)
    return sponsors
