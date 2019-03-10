# -*- coding: utf-8 -*-

from datetime import datetime

from bs4 import BeautifulSoup

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.translation import ugettext as _

from reportlab.pdfgen import canvas

from apps.lan.models import Attendee, LAN
from apps.seating.models import Seat, Seating


def main(request):
    lans = LAN.objects.filter(end_date__gt=datetime.now()).order_by('-start_date')

    if lans:
        return seating_details(request, lans[0].id)

    context = {}
    breadcrumbs = (
        ('studLAN', '/'),
        ('Seatings', reverse('seatings')),
    )
    context['breadcrumbs'] = breadcrumbs

    return render(request, 'seating/seating.html', context)


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
        (lan, ''),
    )
    context['breadcrumbs'] = breadcrumbs

    return render(request, 'seating/seating.html', context)


def seating_details(request, lan_id, seating_id=None, seat_id=None):
    lan = get_object_or_404(LAN, pk=lan_id)
    seatings = Seating.objects.filter(lan=lan)

    if not seatings:
        return render(request, 'seating/seating.html')

    if seating_id:
        seating = get_object_or_404(Seating, pk=seating_id, lan=lan)
    else:
        seating = seatings[0]
        return redirect(seating)

    # users = seating.get_user_registered()
    seats = seating.get_total_seats()

    dom = BeautifulSoup(seating.layout.template, 'html.parser')
    counter = 0
    for tag in dom.find_all('a'):
        children = tag.find_all('rect')
        children[0]['seat-number'] = seats[counter].pk
        children[0]['seat-display'] = seats[counter].placement
        if not seats[counter].user:
            children[0]['class'] = ' seating-node-free'
            children[0]['status'] = 'free'
        else:
            if seats[counter].user == request.user:
                children[0]['class'] = ' seating-node-self'
                children[0]['status'] = 'mine'
            else:
                children[0]['class'] = ' seating-node-occupied'
                children[0]['status'] = 'occupied'
                children[0]['seat-user'] = unicode(seats[counter].user.username)

                # Separate title element for chrome support
                title = dom.new_tag('title')
                title.string = unicode(seats[counter].user.username)
                tag.append(title)

        counter += 1
    dom.encode('utf-8')

    context = {}
    context['seatings'] = seatings
    context['seating'] = seating
    context['seat'] = seat_id
    context['hide_sidebar'] = True
    context['template'] = dom.__str__

    return render(request, 'seating/seating.html', context)


@login_required()
def take(request, seating_id, seat_id):
    seating = get_object_or_404(Seating, pk=seating_id)
    seat = get_object_or_404(Seat, pk=seat_id)
    siblings = list(Seating.objects.filter(lan=seating.lan))
    occupied = seating.get_user_registered()

    if not seating.is_open():
        messages.error(request, _(u'This seatmap is closed.'))
        return redirect(seating)

    for sibling in siblings:
        occupied = occupied + sibling.get_user_registered()

    try:
        attendee = Attendee.objects.get(user=request.user, lan=seating.lan)
    except ObjectDoesNotExist:
        attendee = None
    if (attendee and attendee.has_paid) or seating.lan.has_ticket(request.user):
        if not seating.ticket_types or (seating.lan.has_ticket(request.user) and seating.lan.has_ticket(request.user).ticket_type in seating.ticket_types.all()):
            if not seat.user:
                if request.user in occupied:
                    old_seats = Seat.objects.filter(user=request.user)
                    for os in old_seats:
                        if os.seating.lan == seating.lan:
                            os.user = None
                            os.save()
                seat.user = request.user
                seat.save()
                messages.success(request, _(u'You have successfully reserved your seat.'))
            else:
                messages.error(request, _(u'That seat is reserved by ' + unicode(seat.user)))
        else:
            messages.error(request, _(u'Your ticket does not allow reservation in this seating.'))
    else:
        messages.error(request, _(u'You need to attend and pay before reserving your seat.'))
    return redirect(seating)


@login_required()
def take2(request, lan_id, seating_id, seat_id):
    return take(request, seating_id, seat_id)


@login_required()
def leave(request, seating_id, seat_id):
    seating = get_object_or_404(Seating, pk=seating_id)
    seat = get_object_or_404(Seat, pk=seat_id)

    if not seating.is_open():
        messages.error(request, _(u'This seatmap is closed.'))
        return redirect(seating)

    if seat.user == request.user:
        seat.user = None
        seat.save()
        messages.success(request, _(u'You have unregistered your seat.'))
    else:
        messages.error(request, _(u'This seat is taken.'))
    return redirect(seating)


@staff_member_required
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
            p.drawString(230, cursor, 'Plass ' + unicode(s.placement) + ': ')
            p.drawString(290, cursor, unicode(s.user))
        else:
            p.drawString(230, cursor, 'Plass ' + unicode(s.placement) + ': ')
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


@login_required()
def leave2(request, lan_id, seating_id, seat_id):
    return leave(request, seating_id, seat_id)


@staff_member_required
def seating_map(request, seating_id):
    seating = get_object_or_404(Seating, pk=seating_id)
    lan = get_object_or_404(LAN, id=seating.lan.id)
    seats = list(Seat.objects.filter(seating=seating).order_by('placement'))

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=' + seating.title + '.pdf'

    p = canvas.Canvas(response)

    pagecounter = 0
    for s in seats:
        if pagecounter == 1:
            y_value = 780
            p.showPage()
            pagecounter = 0
        else:
            pagecounter += 1
            y_value = 450

        p.setFont('Helvetica', 30)
        p.drawString(180, y_value, lan.title)
        p.drawString(180, y_value - 80, seating.title)
        if s.user:
            p.drawString(180, y_value - 130, 'Plass ' + unicode(s.placement) + ': ')
            p.drawString(180, y_value - 180, unicode(s.user))
        else:
            p.drawString(180, y_value - 130, 'Plass ' + unicode(s.placement) + ': ')
            p.drawString(180, y_value - 180, '[Ledig]')

    p.save()

    return response
