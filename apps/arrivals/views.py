# -*- encoding: utf-8 -*-

from datetime import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404

from apps.lan.models import LAN, Attendee

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
    
    paid_count = 0
    arrived_count = 0
    for attendee in attendees:
        if attendee.has_paid:
            paid_count += 1
        if attendee.arrived:
            arrived_count += 1

    return render(request, 'arrivals/arrivals.html', {'attendees': attendees, 'lan': lan, 'paid_count' : paid_count, 
        'arrived_count' : arrived_count, 'breadcrumbs': breadcrumbs})

@login_required
def toggle(request, lan_id):
    if request.method == 'GET':
        username = request.GET.get('username')
        toggle_type = request.GET.get('type')
        previous_value = request.GET.get('prev')

        
        lan = get_object_or_404(LAN, pk=lan_id)
        user = get_object_or_404(User, username=username)
        try:
            attendee = Attendee.objects.get(lan=lan, user=user)


            print not 0
            if int(toggle_type) == 0:
                attendee.has_paid = reverse(previous_value)
            elif int(toggle_type) == 1:
                attendee.arrived = reverse(previous_value)
            else:
                return HttpResponse(status=404)            

            attendee.save()

        except Attendee.DoesNotExist:
            messages.error(request, "%s was not found in attendees for %s" % (user, lan))
        
        return HttpResponse(status = 200)
    return HttpResponse(status=404)
    
def reverse(val):
    if val == "True":
        return False
    elif val == "False":
        return True