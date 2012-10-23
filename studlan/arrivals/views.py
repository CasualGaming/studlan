# -*- encoding: utf-8 -*-

from datetime import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404

from studlan.lan.models import LAN, Attendee

@login_required
def home(request):
    if not request.user.is_staff:
        raise Http404
    
    lans = LAN.objects.filter(end_date__gte=datetime.now())
    upcoming = True
    if lans.count() == 1:
        return redirect('arrivals', lan_id=lans[0].id)
    if lans.count == 0:
        lans = LAN.objects.all()
        upcoming = False 

    breadcrumbs = (
        ('studLAN', '/'),
        ('Arrivals', '')
    )

    return render(request, 'arrivals/home.html', {'lans': lans, 'upcoming': upcoming, 'breadcrumbs': breadcrumbs})
    
@login_required
def arrivals(request, lan_id):
    if not request.user.is_staff:
        raise Http404
    
    lan = get_object_or_404(LAN, pk=lan_id)
    attendees = Attendee.objects.filter(lan=lan)

    breadcrumbs = (
        ('studLAN', '/'),
        ('Arrivals', reverse('arrival_home')),
        (lan, ''),
    )

    return render(request, 'arrivals/arrivals.html', {'attendees': attendees, 'lan': lan, 'breadcrumbs': breadcrumbs})

@login_required
def toggle_arrival(request, lan_id, user_id):
    if not request.user.is_staff:
        raise Http404

    lan = get_object_or_404(LAN, pk=lan_id)
    user = get_object_or_404(User, pk=user_id)
    try:
        attendee = Attendee.objects.get(lan=lan, user=user)

        if attendee.arrived:
            attendee.arrived = False
        else:
            attendee.arrived = True
        attendee.save()

    except Attendee.DoesNotExist:
        messages.error(request, "%s was not found in attendees for %s" % (user, lan))

    return redirect('arrivals', lan_id=lan_id)

@login_required
def toggle_paid(request, lan_id, user_id):
    if not request.user.is_staff:
        raise Http404

    lan = get_object_or_404(LAN, pk=lan_id)
    user = get_object_or_404(User, pk=user_id)
    try:
        attendee = Attendee.objects.get(lan=lan, user=user)

        if attendee.has_paid:
            attendee.has_paid = False
        else:
            attendee.has_paid = True
        attendee.save()

    except Attendee.DoesNotExist:
        messages.error(request, "%s was not found in attendees for %s" % (user, lan))

    return redirect('arrivals', lan_id=lan_id)
