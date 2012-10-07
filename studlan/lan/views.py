# -*- coding: utf-8 -*-

from datetime import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404

from studlan.lan.models import LAN, Attendee

def dispatch(request):
    lans = LAN.objects.filter(end_date__gte=datetime.now())
    if lans:
        next_lan = lans[0]
        return redirect('/%s/' % next_lan.slug)
    else:
        return listing(request)

def home(request):
    lans = LAN.objects.filter(end_date__gte=datetime.now())
    if lans:
        next_lan = lans[0]
        return details(request, next_lan.id)
    else:
        return listing(request)

def listing(request):
    lans = LAN.objects.all()

    return render(request, 'lan/list.html', {'lans': lans})

def details(request, lan_id):
    lan = get_object_or_404(LAN, pk=lan_id)

    if request.user in lan.attendees:
        status = 'attending'
    else:
        status = 'open'

    return render(request, 'lan/details.html', {'lan': lan, 'status': status})

def history(request, lan_id, user_id):
    return HttpResponseRedirect('/')

@login_required
def attend(request, lan_id):
    lan = get_object_or_404(LAN, pk=lan_id)
    
    if request.user in lan.attendees:
        messages.error(request, "You are already in the attendee list for %s" % lan)
    else:
        attendee = Attendee(lan=lan, user=request.user)
        attendee.save()

        messages.success(request, "Successfully added you to attendee list for %s" % lan)
        
    return redirect(lan)

@login_required
def unattend(request, lan_id):
    lan = get_object_or_404(LAN, pk=lan_id)
    
    if request.user not in lan.attendees:
        messages.error(request, "You are not in the attendee list for %s" % lan)
    else:
        attendee = Attendee.objects.get(lan=lan, user=request.user)
        attendee.delete()

        messages.success(request, "Successfully removed you from attendee list for %s" % lan)
        
    return redirect(lan)
