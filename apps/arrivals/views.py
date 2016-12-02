# -*- encoding: utf-8 -*-

from datetime import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required

from apps.lan.models import LAN, Attendee, Ticket, TicketType
from apps.seating.models import Seat


@login_required
@staff_member_required
def home(request):
    lans = LAN.objects.filter(end_date__gte=datetime.now())
    if lans.count() == 1:
        return redirect('arrivals', lan_id=lans[0].id)
    else:
        lans = LAN.objects.all()

    breadcrumbs = (
        ('Home', '/'),
        ('Arrivals', '')
    )

    return render(request, 'arrivals/home.html', {'lans': lans, 'breadcrumbs': breadcrumbs})


@ensure_csrf_cookie
@staff_member_required
def arrivals(request, lan_id):
    if not request.user.is_staff:
        raise Http404
    
    lan = get_object_or_404(LAN, pk=lan_id)
    attendees = Attendee.objects.filter(lan=lan)

    breadcrumbs = (
        ('Home', '/'),
        ('Arrivals', reverse('arrival_home')),
        (lan, ''),
    )

    ticket_types = TicketType.objects.filter(lan=lan)
    tickets = Ticket.objects.filter(ticket_type__in=ticket_types)
    user_seats = dict()
    ticket_users = dict()

    for ticket in tickets:
        ticket_users[ticket.user] = ticket
    
    paid_count = 0
    arrived_count = 0
    for attendee in attendees:
        if Seat.objects.filter(user=attendee.user, seating__lan=lan):
            user_seats[attendee] = Seat.objects.get(user=attendee.user, seating__lan=lan)
        if attendee.has_paid:
            paid_count += 1
        if attendee.arrived:
            arrived_count += 1

    paid_count += len(tickets)

    return render(request, 'arrivals/arrivals.html', {'attendees': attendees, 'lan': lan, 
        'paid_count': paid_count, 'arrived_count': arrived_count, 'breadcrumbs': breadcrumbs,
        'tickets': tickets, 'ticket_users': ticket_users, 'user_seats': user_seats})


@staff_member_required
def toggle(request, lan_id):
    if request.method == 'POST':
        username = request.POST.get('username')
        toggle_type = request.POST.get('type')
        previous_value = request.POST.get('prev')

        lan = get_object_or_404(LAN, pk=lan_id)
        user = get_object_or_404(User, username=username)
        try:
            attendee = Attendee.objects.get(lan=lan, user=user)

            if int(toggle_type) == 0:
                attendee.has_paid = reverse(previous_value)
            elif int(toggle_type) == 1:
                attendee.arrived = reverse(previous_value)
            else:
                raise Http404          

            attendee.save()

        except Attendee.DoesNotExist:
            messages.error(request, "%s was not found in attendees for %s" % (user, lan))
        
        return HttpResponse(status=200)
    return HttpResponse(status=404)


def reverse(val):
    if val == "True":
        return False
    elif val == "False":
        return True
