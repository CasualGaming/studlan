# -*- coding: utf-8 -*-

from django import template

from apps.sponsor.models import Sponsor

register = template.Library()

@register.inclusion_tag('sponsor/sponsor_list.html')
def show_sponsor_list():
    sponsors = Sponsor.objects.all()

    return {'sponsors': sponsors}
