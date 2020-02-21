# -*- encoding: utf-8 -*-

from datetime import datetime

from django.contrib.auth.decorators import permission_required
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.utils.translation import ugettext as _
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_POST, require_safe

from apps.lan.models import Attendee, LAN, Ticket
from apps.seating.models import Seat


@require_safe
@permission_required('lan.register_arrivals')
def home(request):
    context = {}
    context['upcoming_lans'] = LAN.objects.filter(end_date__gte=datetime.now()).order_by('start_date')
    context['previous_lans'] = LAN.objects.filter(end_date__lt=datetime.now()).order_by('-start_date')
    return render(request, 'arrivals/home.html', context)


@require_safe
@ensure_csrf_cookie
@permission_required('lan.register_arrivals')
def arrivals(request, lan_id):
    lan = get_object_or_404(LAN, pk=lan_id)
    total_paid_count = 0
    users_set = set()

    # Attendees (incl. paid and arrived)
    attendees = Attendee.objects.filter(lan=lan)
    users_set.update(map(lambda o: o.user, attendees))
    attendee_users = map(lambda d: d['user'], attendees.values('user'))
    paid_users = map(lambda d: d['user'], attendees.filter(has_paid=True).values('user'))
    total_paid_count += len(paid_users)
    arrived_users = map(lambda d: d['user'], attendees.filter(arrived=True).values('user'))

    # Tickets
    tickets = Ticket.objects.filter(ticket_type__lan=lan)
    user_tickets = {}
    for serial_user in tickets.values('user').distinct():
        user = tickets.filter(user=serial_user['user'])[0].user
        users_set.add(user)
        user_tickets[user] = tickets.filter(user=user)
        total_paid_count += len(user_tickets[user])

    # Seats
    seats = Seat.objects.filter(user__isnull=False, seating__lan=lan)
    user_seats = {}
    user_seats_count = 0
    for serial_user in seats.values('user').distinct():
        user = seats.filter(user=serial_user['user'])[0].user
        users_set.add(user)
        user_seats[user] = seats.filter(user=user)
        user_seats_count += len(user_seats[user])

    # Users
    users = sorted(list(users_set), key=lambda user: user.username)

    breadcrumbs = (
        (lan, reverse('lan_details', kwargs={'lan_id': lan.id})), (_(u'Arrivals'), ''),
    )
    context = {
        'breadcrumbs': breadcrumbs,
        'lan': lan,
        'users': users,
        'total_paid_count': total_paid_count,
        'attendee_users': attendee_users,
        'paid_users': paid_users,
        'arrived_users': arrived_users,
        'user_seats': user_seats,
        'user_seats_count': user_seats_count,
        'user_tickets': user_tickets,
    }

    return render(request, 'arrivals/arrivals.html', context)


@require_POST
@permission_required('lan.register_arrivals')
def toggle(request, lan_id):
    username = request.POST.get('username')
    toggle_type = request.POST.get('type')
    previous_value = request.POST.get('prev')

    lan = LAN.objects.filter(pk=lan_id).first()
    if lan is None:
        return HttpResponse(status=404, content=_('LAN not found.'))

    user = User.objects.filter(username=username).first()
    if user is None:
        return HttpResponse(status=404, content=_('User not found.'))

    attendee = Attendee.objects.filter(lan=lan, user=user).first()
    if attendee is None:
        return HttpResponse(status=404, content=_('The user is not attending the LAN.'))

    if int(toggle_type) == 0:
        attendee.has_paid = flip_string_bool(previous_value)
    elif int(toggle_type) == 1:
        attendee.arrived = flip_string_bool(previous_value)
    else:
        return HttpResponse(status=400, content=_('Invalid toggle type.'))

    attendee.save()
    return HttpResponse(status=200)


def flip_string_bool(val):
    if val == 'True':
        return False
    elif val == 'False':
        return True
