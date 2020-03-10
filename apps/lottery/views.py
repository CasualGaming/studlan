# -*- coding: utf-8 -*-

from random import SystemRandom

from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.translation import ugettext as _
from django.views.decorators.http import require_POST, require_safe

from apps.lan.models import Attendee
from apps.userprofile.models import User

from .models import Lottery, LotteryParticipant, LotteryWinner


@require_safe
def details(request, lottery_id):
    lottery = get_object_or_404(Lottery, pk=lottery_id)
    lan = lottery.lan
    participants = User.objects.filter(lotteryparticipant__lottery=lottery).order_by('username')
    winners = [w.user for w in LotteryWinner.objects.filter(lottery=lottery).order_by('id').select_related('user')]
    if winners:
        last_winner = winners[-1]
    else:
        last_winner = None

    breadcrumbs = (
        (lan, lan.get_absolute_url()),
        (_(u'Competitions'), reverse('competitions_lan_compos', kwargs={'lan_id': lan.id})),
        (unicode(lottery), ''),
    )

    return render(request, 'lottery/details.html', {'breadcrumbs': breadcrumbs, 'lottery': lottery,
                  'participants': participants, 'winners': winners, 'last_winner': last_winner})


@require_POST
@login_required
def sign_up(request, lottery_id):
    lottery = get_object_or_404(Lottery, pk=lottery_id)

    if not lottery.registration_open or lottery.is_participating(request.user):
        # No error message needed
        return redirect(lottery)

    if lottery.enforce_payment:
        attendance = Attendee.objects.filter(lan=lottery.lan, user=request.user)
        if not attendance:
            messages.error(request, _(u'You are not signed up for the LAN.'))
            return redirect(lottery)
        has_paid = attendance[0].has_paid or lottery.lan.has_ticket(request.user)
        if not has_paid:
            messages.error(request, _(u'You have not paid for the LAN.'))
            return redirect(lottery)

    LotteryParticipant.objects.create(user=request.user, lottery=lottery)
    return redirect(lottery)


@require_POST
@login_required
def sign_off(request, lottery_id):
    lottery = get_object_or_404(Lottery, pk=lottery_id)
    if lottery.registration_open and lottery.is_participating(request.user):
        LotteryParticipant.objects.filter(user=request.user, lottery=lottery).delete()
    return redirect(lottery)


@require_POST
@permission_required('lottery.open_close')
def open_(request, lottery_id):
    lottery = get_object_or_404(Lottery, pk=lottery_id)
    lottery.registration_open = True
    lottery.save()
    return redirect(lottery)


@require_POST
@permission_required('lottery.open_close')
def close(request, lottery_id):
    lottery = get_object_or_404(Lottery, pk=lottery_id)
    lottery.registration_open = False
    lottery.save()
    return redirect(lottery)


@require_POST
@permission_required('lottery.draw')
def draw(request, lottery_id):
    lottery = get_object_or_404(Lottery, pk=lottery_id)
    participants = lottery.lotteryparticipant_set.all()

    if len(participants) < 1:
        messages.error(request, _(u'No eligible participants.'))
        return redirect(lottery)

    rand = SystemRandom()
    winner_id = rand.randrange(0, len(participants))
    winner = participants[winner_id].user

    if not lottery.multiple_winnings:
        participants[winner_id].delete()

    LotteryWinner.objects.create(user=winner, lottery=lottery)

    return redirect(lottery)
