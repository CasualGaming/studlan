# -*- coding: utf-8 -*-

from datetime import datetime

from bs4 import BeautifulSoup

from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.translation import ugettext as _

from reportlab.lib import pagesizes
from reportlab.pdfgen.canvas import Canvas as PdfCanvas

from apps.lan.models import Attendee, LAN
from apps.seating.models import Seat, Seating


def main(request):
    lans = LAN.objects.filter(end_date__gt=datetime.now()).order_by('-start_date')

    if lans:
        return seating_details(request, lans[0].id)

    return render(request, 'seating/seating.html')


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
        (lan, reverse('lan_details', kwargs={'lan_id': lan.id})),
        (_(u'Seating'), ''),
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
    context['lan'] = lan
    context['seatings'] = seatings
    context['seating'] = seating
    context['seat'] = seat_id
    context['hide_sidebar'] = True
    context['template'] = dom.__str__
    breadcrumbs = (
        (lan, reverse('lan_details', kwargs={'lan_id': lan.id})),
        (_(u'Seating'), ''),
    )
    context['breadcrumbs'] = breadcrumbs

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


@login_required()
def leave2(request, lan_id, seating_id, seat_id):
    return leave(request, seating_id, seat_id)


@permission_required('seating.export_seating')
def seating_list(request, seating_id):
    seating = get_object_or_404(Seating, pk=seating_id)
    lan = get_object_or_404(LAN, id=seating.lan.id)
    seats = list(Seat.objects.filter(seating=seating).order_by('placement'))

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=' + seating.title + '.pdf'

    page_size = pagesizes.A4
    page_width, page_height = page_size
    page_width_center = page_width / 2
    p = PdfCanvas(response, pagesize=page_size)

    cursor_top = page_height - 120
    left_col_offset = 50
    right_col_offset = 300

    # 1 is left, 2 is right
    page_side = 1
    cursor = cursor_top
    new_page = True
    x_offset = left_col_offset
    page_num = 1
    for seat in seats:
        if cursor < 70:
            # Flip to right side or new page
            cursor = cursor_top
            if page_side == 1:
                page_side = 2
                x_offset = right_col_offset
            else:
                page_side = 1
                x_offset = left_col_offset
                new_page = True
                page_num += 1
                p.showPage()

        if new_page:
            new_page = False
            p.setFont('Times-Roman', 25)
            p.drawCentredString(page_width_center, page_height - 60, lan.title)
            p.setFont('Times-Roman', 20)
            p.drawCentredString(page_width_center, page_height - 90, seating.title)
            p.setFont('Helvetica', 14)
            p.drawCentredString(page_width_center, 40, '{0} {1}'.format(_(u'Page'), page_num))
            # For seat text
            p.setFont('Helvetica', 14)

        occupant = unicode(seat.user) if seat.user else ''
        p.drawString(x_offset, cursor, u'{0} {1}: {2}'.format(_(u'Seat'), seat.placement, occupant))

        cursor -= 20

    p.showPage()
    p.save()

    return response


@permission_required('seating.export_seating')
def seating_map(request, seating_id):
    seating = get_object_or_404(Seating, pk=seating_id)
    lan = get_object_or_404(LAN, id=seating.lan.id)
    seats = list(Seat.objects.filter(seating=seating).order_by('placement'))

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=' + seating.title + '.pdf'

    page_size = pagesizes.A4
    page_width, page_height = page_size
    page_width_center = page_width / 2
    page_height_center = page_height / 2
    p = PdfCanvas(response, pagesize=page_size)

    new_page = True
    y_offset = page_height_center
    for seat in seats:
        p.setFont('Times-Roman', 40)
        p.drawCentredString(page_width_center, y_offset + 310, lan.title)
        p.setFont('Times-Roman', 35)
        text = _(u'%(seating)s, seat %(seat)d') % {'seating': seating.title, 'seat': seat.placement}
        p.drawCentredString(page_width_center, y_offset + 250, text)
        if seat.user:
            p.setFont('Helvetica', 40)
            occupant = unicode(seat.user)
        else:
            p.setFont('Helvetica', 40)
            occupant = _(u'(Available)')
        p.drawCentredString(page_width_center, y_offset + 150, occupant)

        if new_page:
            new_page = False
            y_offset = 0
        else:
            new_page = True
            y_offset = page_height_center
            p.showPage()

    p.showPage()
    p.save()

    return response
