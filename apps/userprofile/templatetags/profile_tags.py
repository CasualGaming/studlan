# -*- coding: utf-8 -*-

from django import template


register = template.Library()


@register.inclusion_tag('user/profile_tabs.html')
def profile_tabs(active):
    return {'active': active}


@register.inclusion_tag('user/profile_content.html', takes_context=True)
def profile_content(context):
    return {'user': context['user'], 'quser': context['quser'], 'profile': context['profile'], 'user_seats': context['user_seats'], 'perms': context['perms']}
