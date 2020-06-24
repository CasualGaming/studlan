# -*- encoding: utf-8 -*-

from collections import OrderedDict
from datetime import datetime

from dateutil.relativedelta import relativedelta

from django.contrib.auth.decorators import permission_required
from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import get_object_or_404, render
from django.utils.translation import ugettext as _
from django.views.decorators.http import require_safe

from apps.competition.models import Competition
from apps.lan.models import Attendee, LAN, Ticket, TicketType


@require_safe
@permission_required('lan.show_statistics')
def statistics_list(request):
    context = {}
    context['upcoming_lans'] = LAN.objects.filter(end_date__gte=datetime.now()).order_by('start_date')
    context['previous_lans'] = LAN.objects.filter(end_date__lt=datetime.now()).order_by('-start_date')
    return render(request, 'statistics/list.html', context)


@require_safe
@permission_required('lan.show_statistics')
def statistics(request, lan_id):
    lan = get_object_or_404(LAN, pk=lan_id)

    # Participants (paid or ticket)
    participants = set()
    ticket_users = User.objects.filter(ticket__ticket_type__lan=lan)
    participants.update(ticket_users)
    paid_users = User.objects.filter(attendee__lan=lan, attendee__has_paid=True)
    participants.update(paid_users)

    # Arrivals
    arrived_participants_count = Attendee.objects.filter(lan=lan, user__in=participants, arrived=True).count()

    # Participant ages
    age_counts = {}
    for participant in participants:
        age = relativedelta(lan.start_date.date(), participant.profile.date_of_birth).years
        if age in age_counts:
            age_counts[age] += 1
        else:
            age_counts[age] = 1
    age_counts = OrderedDict(sorted(age_counts.items(), key=lambda t: t[0]))

    # Tickets and paid counts
    ticket_counts = []
    ticket_count_total = 0
    for ticket_type in TicketType.objects.filter(lan=lan):
        count = Ticket.objects.filter(ticket_type=ticket_type).count()
        ticket_count_total += count
        ticket_counts.append((ticket_type, count))
    paid_count = Attendee.objects.filter(lan=lan, has_paid=True).count()
    ticket_paid_total_count = ticket_count_total + paid_count

    # Competitions
    competition_counts = []
    for competition in Competition.objects.filter(lan=lan):
        count = User.objects.filter(
            Q(participant__competition=competition)
            | Q(newteamleader__participant__competition=competition)
            | Q(new_team_members__participant__competition=competition),
        ).count()
        competition_counts.append((competition, count))

    breadcrumbs = (
        (lan, lan.get_absolute_url()),
        (_(u'Statistics'), ''),
    )
    context = {
        'breadcrumbs': breadcrumbs,
        'lan': lan,
        'arrival_count': arrived_participants_count,
        'participant_count': len(participants),
        'age_counts': age_counts,
        'ticket_counts': ticket_counts,
        'paid_count': paid_count,
        'ticket_paid_total_count': ticket_paid_total_count,
        'competition_counts': competition_counts,
    }

    return render(request, 'statistics/lan.html', context)
