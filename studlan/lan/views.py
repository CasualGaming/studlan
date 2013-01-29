# -*- coding: utf-8 -*-

from datetime import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404

from studlan.lan.models import LAN, Attendee

def home(request):
    lans = LAN.objects.filter(end_date__gte=datetime.now())
    if lans.count() == 1:
        next_lan = lans[0]
        return redirect('lan_details', lan_id=next_lan.id)
    else:
        return listing(request)

def listing(request):
    upcoming_lans = LAN.objects.filter(end_date__gte=datetime.now())
    previous_lans = LAN.objects.filter(end_date__lt=datetime.now())

    return render(request, 'lan/list.html', {'upcoming': upcoming_lans, 'previous': previous_lans})

def details(request, lan_id):
    lan = get_object_or_404(LAN, pk=lan_id)

    if request.user in lan.attendees:
        status = 'attending'
    else:
        status = 'open'

    return render(request, 'lan/details.html', {'lan': lan, 'status': status})

@login_required
def attend(request, lan_id):
    lan = get_object_or_404(LAN, pk=lan_id)
    
    if lan.end_date < datetime.now():
        messages.error(request, "This LAN has finished and can no longer be attended")
        return redirect(lan)
    
    if not request.user.get_profile().has_address():
        messages.error(request, "You need to fill in your address and zip code in order to sign up for a LAN.")
    else:
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

    if lan.start_date < datetime.now():
        messages.error(request, "This LAN has already started, you can not retract your signup")
        return redirect(lan)
    
    if request.user not in lan.attendees:
        messages.error(request, "You are not in the attendee list for %s" % lan)
    else:
        attendee = Attendee.objects.get(lan=lan, user=request.user)
        attendee.delete()

        messages.success(request, "Successfully removed you from attendee list for %s" % lan)
        
    return redirect(lan)

@login_required
def attendee_ntnu_usernames(request, lan_id):
    if not request.user.is_staff:
        raise Http404

    else: 
        lan = get_object_or_404(LAN, pk=lan_id)
    
        return render(request, 'lan/attendee_ntnu_usernames.html', {'attendees': lan.attendee_ntnu_usernames})
