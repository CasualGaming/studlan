# -*- coding: utf-8 -*-

from datetime import datetime
import logging

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect, get_object_or_404
from apps.seating.models import Seating, Seat
from apps.lan.models import LAN, Attendee

def main(request):
        context = {}
        lans = LAN.objects.all()
        seatings = Seating.objects.all()
        context['seatings'] = seatings
        context['lans'] = lans
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

    breadcrumbs = (
        ('studLAN', '/'),
        ('Seatings', reverse('seatings')),
        (seating, ''),
    )
    context['seating'] = seating
    context['breadcrumbs'] = breadcrumbs

    users = seating.get_user_registered()
    seats = seating.get_total_seats()

    context['users'] = users
    context['seats'] = seats

    # Insert placeholder image if the image_url is empty
    return render(request, 'seating/seating.html', context)

@login_required()
def join(request, seating_id, seat_id):
    seating = get_object_or_404(Seating, pk=seating_id)
    occupied = seating.get_user_registered()
    seat = get_object_or_404(Seat, pk=seat_id)
    try:
        attendee = Attendee.objects.get(user=request.user)
    except ObjectDoesNotExist:
        attendee = None

    if attendee and attendee.has_paid:

        if request.user in occupied:
            old_seat = get_object_or_404(Seat, user=request.user, seating=seating)
            old_seat.user = None
            old_seat.save()

        seat.user = request.user
        seat.save()
        messages.success(request, "You have successfully reserved your seat! ")
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



# TODO
# Mode these view out of seating and into auth, 
# and make some kind of fallback on the plain forms
def log_in(request):
    username = password = ''
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                messages.success(request, 'You have successfully logged in.')
            else:
                messages.add_message(request, messages.WARNING,
                        'Your account is not active, please try again '
                        'or contact the site admin if the problem '
                        'persists.')
        else:

            messages.add_message(request, messages.ERROR,
                                 'Wrong username/password.')
    return redirect('myprofile')


def log_out(request):
    logout(request)

    messages.success(request, 'You have successfully logged out.')
    return redirect('root')


def register_user(request):

    username = password = fname = lname = email = ''
    if request.POST:
        uname = request.POST.get('username')
        pword = request.POST.get('password')
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        email = request.POST.get('email')
        if uname is not None and pword is not None and fname \
            is not None and lname is not None and email is not None:
            user = User.objects.create_user(username=uname,
                    password=pword, email=email)
            user.set_password(pword)
            user.first_name = fname
            user.last_name = lname
            user.is_active = True
            user.save()

            # TODO review this

            messages.add_message(request, messages.SUCCESS,
                                 'Registration successful. You may now '
                                 'log in.')

    return redirect('root')