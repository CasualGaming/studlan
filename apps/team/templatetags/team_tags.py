# -*- coding: utf-8 -*-

from django import template


register = template.Library()


@register.inclusion_tag('team/team_list.html')
def team_list(teams):
    return {'teams': teams}


@register.inclusion_tag('team/team_tabs.html')
def team_tabs(active):
    return {'active': active}


@register.filter
def is_member(team, user):
    if team.member_set.filter(user=user.id).exists():
        return True
    elif team.leader == user:
        return True

    return False
