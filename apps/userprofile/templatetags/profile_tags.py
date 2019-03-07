# -*- coding: utf-8 -*-

from django import template


register = template.Library()


@register.inclusion_tag('user/profile_tabs.html')
def profile_tabs(active):
    return {'active': active}
