# -*- coding: utf-8 -*-

from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.translation import ugettext as _
from django.views.decorators.http import require_POST, require_safe

from apps.lan.models import Attendee

from .models import Poll, PollOption, PollParticipant


@require_safe
def details(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    lan = poll.lan
    options = PollOption.objects.filter(poll=poll)
    participants = PollParticipant.objects.filter(poll=poll)
    user_participant = participants.filter(user=request.user).first() if request.user.is_authenticated() else None

    option_votes = {}
    option_votes_total = 0
    for option in options:
        votes = participants.filter(option=option).count()
        option_votes[option.id] = votes
        option_votes_total += votes

    breadcrumbs = (
        (lan, lan.get_absolute_url()),
        (_(u'Competitions'), reverse('competitions_lan_compos', kwargs={'lan_id': lan.id})),
        (unicode(poll), ''),
    )
    context = {
        'breadcrumbs': breadcrumbs,
        'poll': poll,
        'user_participant': user_participant,
        'options': options,
        'option_votes': option_votes,
        'option_votes_total': option_votes_total,
    }

    return render(request, 'poll/details.html', context)


@require_POST
@login_required
def vote(request, poll_id, option_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    option = get_object_or_404(PollOption, pk=option_id)

    if not poll.is_open:
        return redirect(poll)

    if poll.enforce_payment:
        attendance = Attendee.objects.filter(lan=poll.lan, user=request.user)
        if not attendance:
            messages.error(request, _(u'You are not signed up for the LAN.'))
            return redirect(poll)
        has_paid = attendance[0].has_paid or poll.lan.has_ticket(request.user)
        if not has_paid:
            messages.error(request, _(u'You have not paid for the LAN.'))
            return redirect(poll)

    # Create or update vote
    participant, created = PollParticipant.objects.get_or_create(
        poll=poll, user=request.user, defaults={'option': option})
    if not created:
        participant.option = option
        participant.save()

    return redirect(poll)


@require_POST
@login_required
def unvote(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    if not poll.is_open:
        redirect(poll)

    participants = PollParticipant.objects.filter(poll=poll, user=request.user)
    if participants.exists():
        participants.first().delete()

    return redirect(poll)


@require_POST
@permission_required('poll.open_close')
def open_(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    poll.is_open = True
    poll.save()
    return redirect(poll)


@require_POST
@permission_required('poll.open_close')
def close(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    poll.is_open = False
    poll.save()
    return redirect(poll)
