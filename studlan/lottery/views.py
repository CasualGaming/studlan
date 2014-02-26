# -*- coding: utf-8 -*-

from datetime import datetime
from random import randint

from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import translation
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from studlan.lottery.models import Lottery, LotteryParticipant, LotteryWinner
from studlan.lan.models import LAN, Attendee

def index(request):
    lans = LAN.objects.filter(end_date__gte=datetime.now())
    if not lans.count() == 1:
        return render(request, 'lottery/lottery.html', {'lan': False})
    next_lan = lans[0]
    lotteries = Lottery.objects.filter(lan=next_lan)
    lotteries_translated = []
    signed = []
    for lottery in lotteries:
        lotteries_translated.append(lottery.get_translation(language = translation.get_language()))
        signed.append(lottery.is_participating(request.user))
    return render(request, 'lottery/lottery.html', {'lan': next_lan, 'lotteries': zip(lotteries, lotteries_translated, signed)})

def sign_up(request, lottery_id):
    lottery = get_object_or_404(Lottery, pk=lottery_id)
    if lottery.registration_open and not lottery.is_participating(request.user):
        LotteryParticipant.objects.create(user=request.user, lottery=lottery)

    return redirect(index)

def sign_off(request, lottery_id):
    lottery = get_object_or_404(Lottery, pk=lottery_id)
    if lottery.registration_open:
        participant = get_object_or_404(LotteryParticipant, user=request.user, lottery=lottery)
        participant.delete()

    return redirect(index)

@login_required
def drawing(request, lottery_id=False):
    winner = False
    if lottery_id:
        lottery = get_object_or_404(Lottery, pk=lottery_id)
    else:
        lottery = Lottery.objects.latest('pk')
    winners = LotteryWinner.objects.filter(lottery=lottery)
    if winners:
        winner = winners[len(winners) -1]
    return render(request, 'lottery/drawing.html',{'lottery':lottery, 'winner': winner}) 
   
@login_required
def draw(request, lottery_id):
    lottery = get_object_or_404(Lottery, pk=lottery_id)
    if lottery.multiple_winnings:
        participants = lottery.lotteryparticipant_set.all()
    else:
        participants = lottery.lotteryparticipant_set.all().exclude(has_won = True)

    print lottery.lotterywinner_set.all()

    if len(participants) < 1:
        messages.error(request, 'No eligible participants')
        return redirect(drawing, lottery_id)
        
    winner_id = randint(0, len(participants) -1)
    winner = participants[winner_id].user
    participants[winner_id].has_won = True
    participants[winner_id].save()
    LotteryWinner.objects.create(user = winner, lottery=lottery)
    return redirect(drawing, lottery_id) 
