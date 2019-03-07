# -*- coding: utf-8 -*-

import json

from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect

from apps.api.models import Key
from apps.lan.models import Attendee, LAN
from apps.userprofile.models import UserProfile


def change_arrived(request, api_key, lan_id, username, status):
    keys = Key.objects.filter(content=api_key)
    if len(keys) != 1:
        messages.error(request, 'Invalid API key.')
        return redirect('/')
    else:
        lan = get_object_or_404(LAN, pk=lan_id)
        userprofile = get_object_or_404(UserProfile, ntnu_username=username)
        user = getattr(userprofile, 'user')
        attendee = get_object_or_404(Attendee, lan=lan, user=user)

        if status == '1':
            attendee.arrived = True
            attendee.save()
            messages.success(request, 'Changed status for "{0}" at LAN "{1}" to "arrived"'.format(user, lan))
        elif status == '0':
            attendee.arrived = False
            attendee.save()
            messages.success(request, 'Changed status for "{0}" at LAN "{1}" to "NOT arrived"'.format(user, lan))
        else:
            messages.warning(request, 'Status "{0}" unrecognized.'.format(status))

        return redirect('/')


def change_paid(request, api_key, lan_id, username, status):
    keys = Key.objects.filter(content=api_key)
    if len(keys) != 1:
        messages.error(request, 'Invalid API key.')
        return redirect('/')
    else:
        lan = get_object_or_404(LAN, pk=lan_id)
        userprofile = get_object_or_404(UserProfile, ntnu_username=username)
        user = getattr(userprofile, 'user')
        attendee = get_object_or_404(Attendee, lan=lan, user=user)

        if status == '1':
            attendee.has_paid = True
            attendee.save()
            messages.success(request, 'Changed status for "{0}" at LAN "{1}" to "paid"'.format(user, lan))
        elif status == '0':
            attendee.has_paid = False
            attendee.save()
            messages.success(request, 'Changed status for "{0}" at LAN "{1}" to "NOT paid"'.format(user, lan))
        else:
            messages.warning(request, 'Status "{0}" unrecognized.'.format(status))

        return redirect('/')


def check_status(request, api_key, lan_id, username):
    keys = Key.objects.filter(content=api_key)
    response_data = {}
    if len(keys) != 1:
        messages.error(request, 'Invalid API key.')
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

    return HttpResponse(json.dumps(response_data), content_type='application/json')
