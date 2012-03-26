# -*- coding: utf-8 -*-

from django import template

register = template.Library()

@register.inclusion_tag('team/team_list.html')
def team_list(teams):
    return {'teams': teams}
