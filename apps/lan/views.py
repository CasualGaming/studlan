#-*- coding: utf-8 -*-

from datetime import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import Http404, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.translation import ugettext as _

from apps.lan.models import LAN, Attendee, Ticket

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

    if lan.end_date > datetime.now():
        active = True
    else:
        active = False

    ticket_types = lan.tickettype_set.all() 

    user_tickets = Ticket.objects.filter(user=request.user.id, ticket_type__in=ticket_types)

    if request.user in lan.attendees:
        if request.user in lan.paid_attendees or user_tickets:
            status = 'paid'
        else:
            status = 'attending'
    else:
        status = 'open'

    return render(request, 'lan/details.html', {'lan': lan, 'status': status, 'active': active, 
        'ticket_types': ticket_types, 'ticket': user_tickets})

@login_required
def attend(request, lan_id):
    lan = get_object_or_404(LAN, pk=lan_id)
    
    if lan.end_date < datetime.now():
        messages.error(request, _(u"This LAN has finished and can no longer be attended"))
        return redirect(lan)
    
    if not request.user.profile.has_address():
        messages.error(request, _(u"You need to fill in your address and zip code in order to sign up for a LAN."))
    else:
        if request.user in lan.attendees:
            messages.error(request, _(u"You are already in the attendee list for ") + unicode(lan))
        else:
            attendee = Attendee(lan=lan, user=request.user)
            attendee.save()

            messages.success(request, _(u"Successfully added you to attendee list for ") + unicode(lan))
        
    return redirect(lan)

@login_required
def unattend(request, lan_id):
    lan = get_object_or_404(LAN, pk=lan_id)

    if lan.start_date < datetime.now():
        messages.error(request, _(u"This LAN has already started, you can not retract your signup"))
        return redirect(lan)
    
    if request.user not in lan.attendees:
        messages.error(request, _(u"You are not in the attendee list for ") + unicode(lan))
    else:
        attendee = Attendee.objects.get(lan=lan, user=request.user)
        attendee.delete()

        messages.success(request, _(u"Successfully removed you from attendee list for ") + unicode(lan))
        
    return redirect(lan)

@login_required
def attendee_ntnu_usernames(request, lan_id):
    if not request.user.is_staff:
        raise Http404

    else: 
        lan = get_object_or_404(LAN, pk=lan_id)
    
        return render(request, 'lan/attendee_ntnu_usernames.html', {'attendees': lan.attendee_ntnu_usernames})

@user_passes_test(lambda u: u.is_staff)
def list_paid(request, lan_id):
    import xlwt
    lan = get_object_or_404(LAN, pk=lan_id)

    response = HttpResponse(content_type="application/ms-excel")
    response["Content-Disposition"] = "attachment; filename=paid_attendees_lan-{0}.xls".format(lan_id)

    doc = xlwt.Workbook(encoding='UTF-8')
    sheet = doc.add_sheet("Betalte deltakere")

    row = 0

    for user in lan.paid_attendees:
        write(sheet, user, row, 'cash')
        row += 1

    tickets = lan.tickets()

    for ticket in tickets:
        write(sheet, ticket.user, row, 'ticket')
        row += 1

    doc.save(response)
    return response

def write(sheet, person, row, payment_type):
    profile = person.profile
    sheet.write(row, 0, "{0} {1}".format(person.first_name.encode("UTF-8"), person.last_name.encode("UTF-8")))
    sheet.write(row, 1, "{0}.{1}.{2}".format(profile.date_of_birth.day, 
                                           profile.date_of_birth.month, 
                                           profile.date_of_birth.year))
    sheet.write(row, 2, profile.address)
    sheet.write(row, 3, profile.zip_code)
    sheet.write(row, 4, person.email)
    sheet.write(row, 5, payment_type)
