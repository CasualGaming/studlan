# -*- coding: utf-8 -*-

import logging
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect, get_object_or_404
from apps.seating.models import Seating, Seat
from apps.lan.models import LAN, Attendee
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from bs4 import BeautifulSoup
from django.db.models import Q

def main(request):
        context = {}
        lans = LAN.objects.all().order_by('-start_date')
        if lans:
            seatings = Seating.objects.filter(lan=lans[0])
            context['seatings'] = seatings
            context['lan'] = lans[0]
            context['active'] = 'all'

        breadcrumbs = (
            ('studLAN', '/'),
            ('Seatings', ''),
        )
        context['breadcrumbs'] = breadcrumbs

        return render(request, 'seating/seatings.html', context)

def main_filtered(request, lan_id):
    lan = get_object_or_404(LAN, pk=lan_id)

    context = {}
    seating = Seating.objects.filter(lan=lan)
    seatings = Seating.objects.all()
    context['seatings'] = seatings
    context['seating'] = seating
    context['active'] = 'all'
    context['lan'] = lan
    
    breadcrumbs = (
        ('studLAN', '/'),
        ('Seatings', reverse('seatings')),
        (lan, '')
    )
    context['breadcrumbs'] = breadcrumbs

    return render(request, 'seating/seatings.html', context)


def seating_details(request, seating_id):
    context = {}
    seating = get_object_or_404(Seating, pk=seating_id)
    users = seating.get_user_registered()
    seats = seating.get_total_seats()
    seatcount = seating.get_total_seats().count

    if seating.layout:
        dom = BeautifulSoup(seating.layout.template, "html.parser")
        counter = 0
        for tag in dom.find_all('a'):
            children = tag.find_all('rect')
            if not seats[counter].user:
                children[0]['class'] = ' seating-node-free'
                tag['xlink:href'] = '/seating/details/' + seating_id + '/info/' + str(seats[counter].id)
                tag['title'] = 'Seat ' + str(seats[counter].placement) + ': Free'
            else:
                if seats[counter].user == request.user:
                    children[0]['class'] = ' seating-node-self'
                    tag['xlink:href'] = '/seating/details/' + seating_id + '/info/' + str(seats[counter].id)
                    tag['title'] = 'Seat ' + str(seats[counter].placement) + ': Your seat'
                else:
                    children[0]['class'] = ' seating-node-occupied'
                    tag['xlink:href'] = '/seating/details/' + seating_id + '/info/' + str(seats[counter].id)
                    tag['title'] = 'Seat ' + str(seats[counter].placement) + ': ' + str(seats[counter].user.first_name)\
                                   + ' ' + str(seats[counter].user.last_name)
            counter += 1
        dom.encode("utf-8")

    if seating.ticket_type and seating.ticket_type != seating.lan.has_ticket(request.user):
        messages.error(request, "Your ticket does not allow reservation in this seating")

    breadcrumbs = (
        ('studLAN', '/'),
        ('Seatings', reverse('seatings')),
        (seating, ''),
    )
    context['seating'] = seating
    context['breadcrumbs'] = breadcrumbs
    context['users'] = users
    context['seats'] = seats
    if seating.layout:
        context['template'] = dom.__str__

    return render(request, 'seating/seating.html', context)


@login_required()
def seat_details(request, seating_id, seat_id):
    context = {}
    seating = get_object_or_404(Seating, pk=seating_id)
    users = seating.get_user_registered()
    seats = seating.get_total_seats()
    seatcount = seating.get_total_seats().count
    seat = get_object_or_404(Seat, pk=seat_id)

    if seating.layout:
        dom = BeautifulSoup(seating.layout.template, "html.parser")
        counter = 0
        for tag in dom.find_all('a'):
            children = tag.find_all('rect')
            if not seats[counter].user:
                children[0]['class'] = ' seating-node-free'
                tag['xlink:href'] = '/seating/details/' + seating_id + '/info/' + str(seats[counter].id)
                tag['title'] = 'Seat ' + str(seats[counter].placement) + ': Free'
            else:
                if seats[counter].user == request.user:
                    children[0]['class'] = ' seating-node-self'
                    tag['xlink:href'] = '/seating/details/' + seating_id + '/info/' + str(seats[counter].id)
                    tag['title'] = 'Seat ' + str(seats[counter].placement) + ': Your seat'
                else:
                    children[0]['class'] = ' seating-node-occupied'
                    tag['xlink:href'] = '/seating/details/' + seating_id + '/info/' + str(seats[counter].id)
                    tag['title'] = 'Seat ' + str(seats[counter].placement) + ': ' + str(seats[counter].user.first_name)\
                                   + ' ' + str(seats[counter].user.last_name)
            if seats[counter] == seat:
                children[0]['class'] += ' seating-node-info'
            counter += 1
        dom.encode("utf-8")



    breadcrumbs = (
        ('studLAN', '/'),
        ('Seatings', reverse('seatings')),
        (seating, ''),
    )
    context['seating'] = seating
    context['breadcrumbs'] = breadcrumbs
    context['users'] = users
    context['seats'] = seats
    context['info_seat'] = seat
    if seating.layout:
        context['template'] = dom.__str__

    return render(request, 'seating/seating.html', context)

@login_required()
def join(request, seating_id, seat_id):
    seating = get_object_or_404(Seating, pk=seating_id)
    seat = get_object_or_404(Seat, pk=seat_id)
    siblings = list(Seating.objects.filter(lan=seating.lan))
    occupied = seating.get_user_registered()
    for sibling in siblings:
        occupied = occupied + sibling.get_user_registered()
    try:
        attendee = Attendee.objects.get(user=request.user, lan=seating.lan)
    except ObjectDoesNotExist:
        attendee = None

    if (attendee and attendee.has_paid) or seating.lan.has_ticket(request.user):
        if seating.ticket_type and seating.lan.has_ticket(request.user).ticket_type == seating.ticket_type:
            if seat.is_empty():
                if request.user in occupied:
                    old_seats = Seat.objects.filter(user=request.user)
                    for os in old_seats:
                        if os.seating.lan == seating.lan:
                            os.user = None
                            os.save()
                seat.user = request.user
                seat.save()
                messages.success(request, "You have successfully reserved your seat! ")
            else:
                messages.error(request, "That seat is reserved by " + str(seat.user))
        else:
            messages.error(request, "Your ticket does not allow reservation in this seating")
    else:
        messages.error(request, "You need to attend and pay before reserving your seat")
    return redirect(seating)

@login_required()
def leave(request, seating_id, seat_id):
    seating = get_object_or_404(Seating, pk=seating_id)
    seat = get_object_or_404(Seat, pk=seat_id)
    if seat.user == request.user:
        seat.user = None
        seat.save()
        messages.warning(request, "You have unregistered your seat")
    else:
        messages.error(request, "This seat is taken")
    return redirect(seating)


def log_in(request):
    return redirect('auth_login')


def log_out(request):
    logout(request)

    messages.success(request, 'You have successfully logged out.')
    return redirect('root')


def register_user(request):
    return redirect('auth_register')


def seating_list(request, seating_id):
    seating = get_object_or_404(Seating, pk=seating_id)
    lan = get_object_or_404(LAN, id=seating.lan.id)
    seats = list(Seat.objects.filter(seating=seating).order_by('placement'))

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=' + seating.title + '.pdf'

    p = canvas.Canvas(response)

    p.drawString(230, 820, lan.title)
    p.drawString(230, 800, seating.title)
    cursor = 750
    for s in seats:
        if s.user:
            p.drawString(230, cursor, "Plass " + str(s.placement) + ": ")
            p.drawString(290, cursor, str(s.user))
        else:
            p.drawString(230, cursor, "Plass " + str(s.placement) + ": ")
            p.drawString(290, cursor, '[Ledig]')
        cursor -= 19
        if cursor < 50:
            p.showPage()
            p.drawString(230, 820, lan.title)
            p.drawString(230, 800, seating.title)
            cursor = 750

    p.showPage()
    p.save()

    return response


def seating_map(request, seating_id):
    seating = get_object_or_404(Seating, pk=seating_id)
    lan = get_object_or_404(LAN, id=seating.lan.id)
    seats = list(Seat.objects.filter(seating=seating).order_by('placement'))

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=' + seating.title

    p = canvas.Canvas(response)

    pagecounter = 0
    y_value = 780
    for s in seats:
        if pagecounter == 1:
            y_value = 780
            p.showPage()
            pagecounter = 0
        else:
            pagecounter += 1
            y_value = 450

        p.setFont("Helvetica", 30)
        p.drawString(180, y_value, lan.title)
        p.drawString(180, y_value-80, seating.title)
        if s.user:
            p.drawString(180, y_value-130, "Plass " + str(s.placement) + ": ")
            p.drawString(180, y_value-180, str(s.user))
        else:
            p.drawString(180, y_value-130, "Plass " + str(s.placement) + ": ")
            p.drawString(180, y_value-180, '[Ledig]')

    p.save()

    return response