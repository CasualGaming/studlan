# -*- coding: utf-8 -*-

from django import template


register = template.Library()


@register.inclusion_tag('user/profile_tabs.html')
def profile_tabs(active):
    return {'active': active}


@register.inclusion_tag('user/profile_content.html', takes_context=True)
def profile_content(context, quser, profile, user_seats):
    return {'user': context['user'], 'quser': quser, 'profile': profile, 'user_seats': user_seats}
