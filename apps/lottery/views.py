# -*- coding: utf-8 -*-

from random import randint

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.conf import settings
from django.core.urlresolvers import reverse

from apps.lottery.models import Lottery, LotteryParticipant, LotteryWinner


def lottery_details(request, lottery_id):
    lottery = Lottery.objects.get(pk=lottery_id)

    participants = [participant.user for participant in lottery.lotteryparticipant_set.all()]

    breadcrumbs = (
        (settings.SITE_NAME, '/'),
        ('Events', reverse('competitions')),
        (lottery, ''),
    )

    return render(request, 'lottery/lottery_details.html', {'lottery': lottery, 
                  'participants': participants, 'breadcrumbs': breadcrumbs})


def sign_up(request, lottery_id):
    lottery = get_object_or_404(Lottery, pk=lottery_id)
    if lottery.registration_open and not lottery.is_participating(request.user):
        LotteryParticipant.objects.create(user=request.user, lottery=lottery)

    return redirect(lottery)


def sign_off(request, lottery_id):
    lottery = get_object_or_404(Lottery, pk=lottery_id)
    if lottery.registration_open:
        participant = get_object_or_404(LotteryParticipant, user=request.user, lottery=lottery)
        participant.delete()

    return redirect(lottery)


@staff_member_required
def drawing(request, lottery_id=False):
    winner = False
    if lottery_id:
        lottery = get_object_or_404(Lottery, pk=lottery_id)
    else:
        lottery = Lottery.objects.latest('pk')

    winners = LotteryWinner.objects.filter(lottery=lottery)
    if winners:
        winner = winners[len(winners) - 1]
    return render(request, 'lottery/drawing.html', {'lottery': lottery, 'winner': winner})


@staff_member_required
def draw(request, lottery_id):
    lottery = get_object_or_404(Lottery, pk=lottery_id)
    if lottery.multiple_winnings:
        participants = lottery.lotteryparticipant_set.all()
    else:
        participants = lottery.lotteryparticipant_set.all().exclude(has_won=True)

    print lottery.lotterywinner_set.all()

    if len(participants) < 1:
        messages.error(request, 'No eligible participants')
        return redirect(drawing, lottery_id)
        
    winner_id = randint(0, len(participants) - 1)
    winner = participants[winner_id].user
    participants[winner_id].has_won = True
    participants[winner_id].save()
    LotteryWinner.objects.create(user=winner, lottery=lottery)
    return redirect(drawing, lottery_id) 
