# -*- coding: utf-8 -*-

import json

from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.utils.translation import ugettext as _
from django.views.decorators.http import require_POST, require_safe

from apps.api.models import Key
from apps.lan.models import Attendee, LAN
from apps.userprofile.models import UserProfile


@require_POST
def change_arrived(request, api_key, lan_id, username, status):
    keys = Key.objects.filter(content=api_key)
    if len(keys) != 1:
        messages.error(request, _(u'Invalid API key.'))
        return redirect('/')
    else:
        lan = get_object_or_404(LAN, pk=lan_id)
        userprofile = get_object_or_404(UserProfile, ntnu_username=username)
        user = getattr(userprofile, 'user')
        attendee = get_object_or_404(Attendee, lan=lan, user=user)

        if status == '1':
            attendee.arrived = True
            attendee.save()
            messages.success(request, _(u'Changed status for user "{user}" at LAN "{lan}" to "arrived"').format(user=user, lan=lan))
        elif status == '0':
            attendee.arrived = False
            attendee.save()
            messages.success(request, _(u'Changed status for user "{user}" at LAN "{lan}" to "NOT arrived"').format(user=user, lan=lan))
        else:
            messages.warning(request, _(u'Status "{status}" unrecognized.').format(status=status))

        return redirect('/')


@require_POST
def change_paid(request, api_key, lan_id, username, status):
    keys = Key.objects.filter(content=api_key)
    if len(keys) != 1:
        messages.error(request, _(u'Invalid API key.'))
        return redirect('/')
    else:
        lan = get_object_or_404(LAN, pk=lan_id)
        userprofile = get_object_or_404(UserProfile, ntnu_username=username)
        user = getattr(userprofile, 'user')
        attendee = get_object_or_404(Attendee, lan=lan, user=user)

        if status == '1':
            attendee.has_paid = True
            attendee.save()
            messages.success(request, _(u'Changed status for user "{user}" at LAN "{lan}" to "paid"').format(user=user, lan=lan))
        elif status == '0':
            attendee.has_paid = False
            attendee.save()
            messages.success(request, _(u'Changed status for user "{user}" at LAN "{lan}" to "NOT paid"').format(user=user, lan=lan))
        else:
            messages.warning(request, _(u'Status "{status}" unrecognized.').format(status=status))

        return redirect('/')


@require_safe
def check_status(request, api_key, lan_id, username):
    keys = Key.objects.filter(content=api_key)
    response_data = {}
    if len(keys) != 1:
        messages.error(request, _(u'Invalid API key.'))
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
