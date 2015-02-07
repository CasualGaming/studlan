
from datetime import datetime
import logging

from django import template
from django.utils.translation import ugettext as _
from apps.competition.models import Competition
from apps.lan.models import LAN
from django.db.models import Q

register = template.Library()

#--- For competition ---

@register.inclusion_tag('competition/competition_tabs.html')
def competition_tabs(activities, active):
    return {'activities': activities, 'active': active}

@register.filter
def show_solo_note(compo, user):
    if not compo.has_participant(user):
        return True
    else:	
        participant = compo.participant_set.filter(user=user)
        if participant:
            return not participant[0].is_team()

    return False

#--- For sidebar ---


def do_num_of_competitions(parser, token):
    lans = LAN.objects.filter(end_date__gte=datetime.now())
    if lans.count() < 1:
        return Competition_Renderer(0)
    else:
        return Competition_Renderer(Competition.objects.filter(lan=lans[0]).count())


def get_user_competitions(parser, token):
    return user_in_Renderer()


class user_in_Renderer(template.Node):
    def render(self, context):
        user = context['request'].user

        string = "<li class=\"sidebar-header\"><a href=\"#\">" + _(u"My competitions") + "</a></li>"
        count = 0

        for competition in Competition.objects.filter(~Q(status=4)):
            if competition.has_participant(user):
                string += "<li><a href=\"" + competition.get_absolute_url() + "\">" + unicode(competition) + "</a></li>"
                count += 1

        if not count:
            string = ""

        return string


class Competition_Renderer(template.Node):
    def __init__(self, num_of_competitions):
        self.num_of_competitions = num_of_competitions

    def render(self, context):
        return self.num_of_competitions


register.tag('num_of_competitions', do_num_of_competitions)
register.tag('user_competitions', get_user_competitions)