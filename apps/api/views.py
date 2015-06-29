# -*- coding: utf-8 -*-

import json

from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404
from django.http import HttpResponse


from apps.api.models import Key
from apps.lan.models import LAN, Attendee
from apps.userprofile.models import UserProfile


def change_arrived(request, api_key, lan_id, username, status):
    keys = Key.objects.filter(content=api_key)
    if len(keys) != 1:
        messages.error(request, "Invalid API key.")
        return redirect('/')
    else:
        lan = get_object_or_404(LAN, pk=lan_id)
        userprofile = get_object_or_404(UserProfile, ntnu_username=username)
        user = getattr(userprofile, 'user')
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

        return redirect('/')


def change_paid(request, api_key, lan_id, username, status):
    keys = Key.objects.filter(content=api_key)
    if len(keys) != 1:
        messages.error(request, "Invalid API key.")
        return redirect('/')
    else:
        lan = get_object_or_404(LAN, pk=lan_id)
        userprofile = get_object_or_404(UserProfile, ntnu_username=username)
        user = getattr(userprofile, 'user')
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

        return redirect('/')


def check_status(request, api_key, lan_id, username):
    keys = Key.objects.filter(content=api_key)
    response_data = {}
    if len(keys) != 1:
        messages.error(request, "Invalid API key.")
        return redirect('/')
    else:
        lan = get_object_or_404(LAN, pk=lan_id)
        userprofile = get_object_or_404(UserProfile, ntnu_username=username)
        user = getattr(userprofile, 'user')
        attendee = get_object_or_404(Attendee, lan=lan, user=user)

        if attendee.has_paid:
            response_data['paid'] = ['1']
        else:
            response_data['paid'] = ['0']

        if attendee.has_arrived:
            response_data['arrived'] = ['1']
        else:
            response_data['paid'] = ['0']

    return HttpResponse(json.dumps(response_data), content_type="application/json")