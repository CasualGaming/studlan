# -*- coding: utf-8 -*-

from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404

from studlan.lottery.models import Lottery, Participant, Winner

def index(request):
    lottery = get_object_or_404(Lottery, pk=lottery_id)
    if request.user in lottery.participants:
        signed_up = True
    else:
        signed_up = False

    return render(request, 'lottery/lottery.html', {'lottery': lottery, 'signed_up': signed_up})


def sign_up(request, lottery_id):
    lottery = get_object_or_404(Lottery, pk=lottery_id)
    if lottery.registration_open:
        Participant.objects.create(user=request.user, lottery=lottery)

    return render(index)

def sign_off(request, lottery_id):
    lottery = get_object_or_404(Lottery, pk=lottery_id)
    if lottery.registration_open:
        participant = get_object_or_404(Participant, user=request.user, lottery=lottery)
        participant.objects.delete()

    return render(index)
    
