# -*- coding: utf-8 -*-

from django.contrib import messages
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404

from studlan.api.models import Key
from studlan.lan.models import LAN, Attendee

def change_arrived(request, api_key, lan_id, username, status):
    keys = Key.objects.filter(content=api_key)
    if len(keys) != 1:
        messages.error(request, "Invalid API key.")
        return redirect('/')
    else:
        lan = get_object_or_404(LAN, pk=lan_id)
        user = get_object_or_404(User, username=username)
        attendee = get_object_or_404(Attendee, lan=lan, user=user)
        
        if status == '1':
            attendee.arrived = True
            attendee.save()
            messages.success(request, "Changed status for '%s' at LAN '%s' to 'arrived'" % (user, lan))
        elif status == '0':
            attendee.arrived = False
            attendee.save()
            messages.success(request, "Changed status for '%s' at LAN '%s' to 'NOT arrived'" % (user, lan))
        else:
            messages.warning(request, "Status '%s' unrecognized." % status)

        messages.success(request, "lan/deltakelse finnes.")
        return redirect('/')

def change_paid(request, api_key, lan_id, username, status):
    keys = Key.objects.filter(content=api_key)
    if len(keys) != 1:
        messages.error(request, "Invalid API key.")
        return redirect('/')
    else:
        lan = get_object_or_404(LAN, pk=lan_id)
        user = get_object_or_404(User, username=username)
        attendee = get_object_or_404(Attendee, lan=lan, user=user)
        
        if status == '1':
            attendee.has_paid = True
            attendee.save()
            messages.success(request, "Changed status for '%s' at LAN '%s' to 'paid'" % (user, lan))
        elif status == '0':
            attendee.has_paid = False
            attendee.save()
            messages.success(request, "Changed status for '%s' at LAN '%s' to 'NOT paid'" % (user, lan))
        else:
            messages.warning(request, "Status '%s' unrecognized." % status)

        messages.success(request, "lan/deltakelse finnes.")
        return redirect('/')


