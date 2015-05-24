# -*- coding: utf-8 -*-

from datetime import datetime

from django import template

from apps.lan.models import Attendee, LAN, Stream


register = template.Library()   


@register.filter
def is_attending(user):

    lans = LAN.objects.filter(end_date__gte=datetime.now())

    if lans:
        return Attendee.objects.filter(lan__in=lans, user=user.id)
    else:
        return False


@register.filter
def active_stream():
    streams = Stream.objects.filter(active=True)[:1]
    if streams:
        return streams
    else:
        return False