# -*- coding: utf-8 -*-

from django.http import HttpResponseRedirect
from django.shortcuts import render

from studlan.lan.models import LAN

def list(request):
    lans = LAN.objects.all()

    return render(request, 'lan/list.html', {'lans': lans})

def details(request, lan_id):
    return HttpResponseRedirect('/')

def history(request, lan_id, user_id):
    return HttpResponseRedirect('/')
