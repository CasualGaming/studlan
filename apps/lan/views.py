# -*- coding: utf-8 -*-

from datetime import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.translation import pgettext, ugettext as _

from apps.lan.models import Attendee, Directions, LAN, Ticket


def home(request):
    lans = LAN.objects.filter(end_date__gte=datetime.now())
    if lans.count() == 1:
        next_lan = lans[0]
        return redirect('lan_details', lan_id=next_lan.id)
    else:
        return redirect('lan_listing')


def listing(request):
    context = {}
    context['upcoming'] = LAN.objects.filter(end_date__gte=datetime.now()).order_by('start_date')
    context['previous'] = LAN.objects.filter(end_date__lt=datetime.now()).order_by('-start_date')

    return render(request, 'lan/list.html', context)


def details_id(request, lan_id):
    lan = get_object_or_404(LAN, pk=lan_id)
    if lan.slug:
        return redirect(lan)
    return details(request, lan)


def details_slug(request, lan_slug):
    lan = get_object_or_404(LAN, slug=lan_slug)
    return details(request, lan)


def details(request, lan):
    if lan.end_date > datetime.now():
        active = True
    else:
        active = False

    ticket_types = lan.tickettype_set.all().order_by('-priority', '-price')

    user_tickets = Ticket.objects.filter(user=request.user.id, ticket_type__in=ticket_types)

    directions = Directions.objects.filter(lan=lan)

    if request.user in lan.attendees:
        if request.user in lan.paid_attendees or user_tickets:
            status = 'paid'
        else:
            status = 'attending'
    else:
        status = 'open'

    return render(request, 'lan/details.html', {'lan': lan, 'status': status, 'active': active, 'ticket_types': ticket_types, 'ticket': user_tickets, 'directions': directions})


@login_required
def attend(request, lan_id):
    lan = get_object_or_404(LAN, pk=lan_id)

    if lan.end_date < datetime.now():
        messages.error(request, _(u'This LAN has finished and can no longer be attended.'))
        return redirect(lan)

    if not request.user.profile.has_address():
        messages.error(request, _(u'You need to fill in your address and postal code in order to sign up for a LAN.'))
    else:
        if request.user in lan.attendees:
            messages.error(request, _(u'You are already in the attendee list for {lan}.').format(lan=lan))
        else:
            attendee = Attendee(lan=lan, user=request.user)
            attendee.save()

            messages.success(request, _(u'Successfully added you to attendee list for {lan}.').format(lan=lan))

    return redirect(lan)


@login_required
def unattend(request, lan_id):
    lan = get_object_or_404(LAN, pk=lan_id)

    if lan.start_date < datetime.now():
        messages.error(request, _(u'This LAN has already started, you can\'t retract your signup.'))
        return redirect(lan)

    if request.user not in lan.attendees:
        messages.error(request, _(u'You are not in the attendee list for the LAN.'))
        return redirect(lan)

    ticket_types = lan.tickettype_set.all().order_by('-priority', '-price')
    user_tickets = Ticket.objects.filter(user=request.user.id, ticket_type__in=ticket_types)

    if request.user in lan.paid_attendees or user_tickets:
        messages.error(request, _(u'You cannot remove attendance since you have paid for a ticket to the LAN.'))
        return redirect(lan)
    else:
        attendee = Attendee.objects.get(lan=lan, user=request.user)
        attendee.delete()

        messages.success(request, _(u'Successfully removed you from attendee list for {lan}.').format(lan=lan))

    return redirect(lan)


@permission_required('lan.export_paying_participants')
def list_paid(request, lan_id):
    import xlwt
    lan = get_object_or_404(LAN, pk=lan_id)

    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = u'attachment; filename=paying-participants_lan-{0}.xls'.format(lan_id)

    doc = xlwt.Workbook(encoding='UTF-8')
    sheet = doc.add_sheet(_(u'Paying participants'))

    def write(sheet, person, row, payment_type):
        profile = person.profile
        sheet.write(row, 0, u'{0} {1}'.format(person.first_name, person.last_name))
        sheet.write(row, 1, u'{0}.{1}.{2}'.format(profile.date_of_birth.day, profile.date_of_birth.month, profile.date_of_birth.year))
        sheet.write(row, 2, profile.address)
        sheet.write(row, 3, profile.zip_code)
        sheet.write(row, 4, person.email)
        sheet.write(row, 5, payment_type)

    row = 0

    for user in lan.paid_attendees:
        write(sheet, user, row, pgettext(u'payment type', u'cash'))
        row += 1

    tickets = lan.tickets()
    for ticket in tickets:
        write(sheet, ticket.user, row, pgettext(u'payment type', u'ticket'))
        row += 1

    doc.save(response)
    return response
