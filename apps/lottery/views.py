# -*- coding: utf-8 -*-

from random import SystemRandom

from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.core.urlresolvers import reverse
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.translation import ugettext as _

from apps.lottery.models import Lottery, LotteryParticipant, LotteryWinner


def details(request, lottery_id):
    lottery = get_object_or_404(Lottery, pk=lottery_id)
    lan = lottery.lan
    participants = [participant.user for participant in lottery.lotteryparticipant_set.all()]

    breadcrumbs = (
        (lan, reverse('lan_details', kwargs={'lan_id': lan.id})),
        (_(u'Lottery'), ''),
    )

    return render(request, 'lottery/details.html', {'lottery': lottery,
                  'participants': participants, 'breadcrumbs': breadcrumbs})


@login_required
def sign_up(request, lottery_id):
    lottery = get_object_or_404(Lottery, pk=lottery_id)
    if lottery.registration_open and not lottery.is_participating(request.user):
        LotteryParticipant.objects.create(user=request.user, lottery=lottery)

    return redirect(lottery)


@login_required
def sign_off(request, lottery_id):
    lottery = get_object_or_404(Lottery, pk=lottery_id)
    if lottery.registration_open:
        participant = get_object_or_404(LotteryParticipant, user=request.user, lottery=lottery)
        participant.delete()

    return redirect(lottery)


@permission_required('lottery.draw')
def drawing(request, lottery_id=False):
    winner = False
    if lottery_id:
        lottery = get_object_or_404(Lottery, pk=lottery_id)
    elif Lottery.objects.count() > 0:
        lottery = Lottery.objects.latest('pk')
    else:
        raise Http404('No lotteries exist')

    winners = LotteryWinner.objects.filter(lottery=lottery)
    if winners:
        winner = winners[len(winners) - 1]
    return render(request, 'lottery/drawing.html', {'lottery': lottery, 'winner': winner})


@permission_required('lottery.draw')
def draw(request, lottery_id):
    lottery = get_object_or_404(Lottery, pk=lottery_id)
    if lottery.multiple_winnings:
        participants = lottery.lotteryparticipant_set.all()
    else:
        participants = lottery.lotteryparticipant_set.all().exclude(has_won=True)

    if len(participants) < 1:
        messages.error(request, 'No eligible participants')
        return redirect(drawing, lottery_id)

    rand = SystemRandom()
    winner_id = rand.randrange(0, len(participants))
    winner = participants[winner_id].user
    participants[winner_id].has_won = True
    participants[winner_id].save()
    LotteryWinner.objects.create(user=winner, lottery=lottery)
    return redirect(drawing, lottery_id)
