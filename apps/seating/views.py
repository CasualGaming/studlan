# -*- coding: utf-8 -*-

from datetime import datetime

from bs4 import BeautifulSoup

from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.translation import ugettext as _
from django.views.decorators.http import require_POST, require_safe

from reportlab.lib import pagesizes
from reportlab.pdfgen.canvas import Canvas as PdfCanvas

from apps.lan.models import Attendee, LAN
from apps.seating.models import Seat, Seating


@require_safe
def main(request):
    lans = LAN.objects.filter(end_date__gt=datetime.now()).order_by('-start_date')

    if lans.count() == 1:
        next_lan = lans[0]
        return redirect('seating_details', lan_id=next_lan.id)
    else:
        return redirect('seating_lan_list')


@require_safe
def lan_list(request):
    context = {}
    context['upcoming_lans'] = LAN.objects.filter(end_date__gte=datetime.now()).order_by('start_date')
    context['previous_lans'] = LAN.objects.filter(end_date__lt=datetime.now()).order_by('-start_date')

    return render(request, 'seating/lan_list.html', context)


@require_safe
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
        (lan, lan.get_absolute_url()),
        (_(u'Seating'), ''),
    )
    context['breadcrumbs'] = breadcrumbs

    return render(request, 'seating/seating.html', context)


@require_safe
def seating_details(request, lan_id, seating_id=None, seat_id=None):
    lan = get_object_or_404(LAN, pk=lan_id)
    seatings = Seating.objects.filter(lan=lan)

    if not seating_id:
        if seatings:
            seating = seatings[0]
            return redirect(seating)
        else:
            return render(request, 'seating/seating.html')

    seating = get_object_or_404(Seating, pk=seating_id, lan=lan)
    seats = seating.get_total_seats()

    dom = BeautifulSoup(seating.layout.template, 'html.parser')
    seat_counter = 0
    for tag in dom.find_all('a'):
        seat_counter += 1
        seat_qs = seats.filter(placement=seat_counter)
        if not seat_qs.exists():
            continue

        seat = seat_qs[0]
        children = tag.find_all('rect')
        children[0]['seat-number'] = seat.pk
        children[0]['seat-display'] = seat.placement
        if not seat.user:
            children[0]['class'] = ' seating-node-free'
            children[0]['status'] = 'free'
        else:
            if seat.user == request.user:
                children[0]['class'] = ' seating-node-self'
                children[0]['status'] = 'mine'
            else:
                children[0]['class'] = ' seating-node-occupied'
                children[0]['status'] = 'occupied'
                children[0]['seat-user'] = unicode(seat.user.username)

                # Separate title element for chrome support
                title = dom.new_tag('title')
                title.string = unicode(seat.user.username)
                tag.append(title)

    dom.encode('utf-8')

    context = {}
    context['lan'] = lan
    context['seatings'] = seatings
    context['seating'] = seating
    context['seat'] = seat_id
    if request.user.is_authenticated:
        context['user_ticket_types'] = seating.ticket_types.filter(ticket__user=request.user)
    context['hide_sidebar'] = True
    context['template'] = dom.__str__
    context['breadcrumbs'] = (
        (lan, lan.get_absolute_url()),
        (_(u'Seating'), ''),
    )

    return render(request, 'seating/seating.html', context)


@require_POST
@login_required()
def take_seat(request, seating_id):
    seating = get_object_or_404(Seating, pk=seating_id)
    lan = seating.lan
    if not seating.is_open():
        messages.error(request, _(u'The seating is closed.'))
        return redirect(seating)

    seat_id = get_post_seat_id(request, seating)
    if not seat_id:
        return redirect(seating)
    seat = get_object_or_404(Seat, pk=seat_id)

    siblings = list(Seating.objects.filter(lan=lan))
    occupied = seating.get_user_registered()
    for sibling in siblings:
        occupied = occupied + sibling.get_user_registered()

    try:
        attendee = Attendee.objects.get(user=request.user, lan=lan)
    except ObjectDoesNotExist:
        attendee = None
    if (attendee and attendee.has_paid) or lan.has_ticket(request.user):
        if not seating.ticket_types or (lan.has_ticket(request.user) and lan.has_ticket(request.user).ticket_type in seating.ticket_types.all()):
            if not seat.user:
                if request.user in occupied:
                    old_seats = Seat.objects.filter(user=request.user)
                    for os in old_seats:
                        if os.seating.lan == lan:
                            os.user = None
                            os.save()
                seat.user = request.user
                seat.save()
                messages.success(request, _(u'You have reserved your seat.'))
            else:
                messages.error(request, _(u'That seat is already taken.'))
        else:
            messages.warning(request, _(u'Your ticket does not work in this seating area.'))
    else:
        messages.warning(request, _(u'You need a ticket before reserving a seat.'))
        return redirect(lan)
    return redirect(seating)


@require_POST
@login_required()
def leave_seat(request, seating_id):
    seating = get_object_or_404(Seating, pk=seating_id)
    if not seating.is_open():
        messages.error(request, _(u'The seating is closed.'))
        return redirect(seating)

    seat_id = get_post_seat_id(request, seating)
    if not seat_id:
        return redirect(seating)
    seat = get_object_or_404(Seat, pk=seat_id)

    if seat.user == request.user:
        seat.user = None
        seat.save()
        messages.success(request, _(u'You have unreserved your seat.'))
    else:
        messages.error(request, _(u'This is not your seat.'))
    return redirect(seating)


def get_post_seat_id(request, seating):
    seat_id_str = request.POST.get('seat')
    if not seat_id_str:
        messages.error(request, _(u'No seat was specified.'))
        return None
    try:
        seat_id = int(seat_id_str)
    except ValueError:
        messages.error(request, _(u'Illegal seat.'))
        return None
    return seat_id


@require_safe
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


@require_safe
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
