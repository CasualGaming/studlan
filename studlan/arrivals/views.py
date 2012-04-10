# -*- encoding: utf-8 -*-

from datetime import datetime

from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404


from studlan.lan.models import LAN, Attendee

def home(request):
    if not request.user.is_staff:
        raise Http404
    
    lans = LAN.objects.filter(end_date__gte=datetime.now())
    upcoming = True
    if lans.count() == 1:
        return redirect(lans[0])
    if lans.count == 0:
        lans = LAN.objects.all()
        upcoming = False 

    return render(request, 'arrivals/home.html', {'lans': lans, 'upcoming': upcoming})
    

def arrivals(request, lan_id):
    if not request.user.is_staff:
        raise Http404
    
    lan = get_object_or_404(LAN, pk=lan_id)
    attendees = Attendee.objects.filter(lan=lan)

    # This is the old sorting code for the user entries. It should be obsolete since ordering
    # is now done on the model layer.
    #users = User.objects.all()
    #sorted_users = []
    #for u in users:
    #    sorted_users.append(u)
    #sorted_users.sort(key=lambda x: x.username.lower(), reverse=False)

    return render(request, 'arrivals/arrivals.html', {'attendees': attendees, 'lan': lan})
 
def toggle_arrival(request, lan_id, user_id):
    if not request.user.is_staff:
        raise Http404

    lan = get_object_or_404(LAN, pk=lan_id)
    user = get_object_or_404(User, pk=user_id)
    try:
        attendee = Attendee.objects.get(lan=lan, user=user)

        if attendee.has_paid:
            print 'had paid'
            attendee.has_paid = False
        else:
            print 'had not paid'
            attendee.has_paid = True
        attendee.save()

    except Attendee.DoesNotExist:
        messages.error(request, "%s was not found in attendees for %s" % (user, lan))

    return redirect('arrivals', lan_id=lan_id)
