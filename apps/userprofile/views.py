    # -*- coding: utf-8 -*-

from datetime import datetime

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.translation import ugettext as _

from apps.lan.models import Attendee, LAN
from apps.userprofile.forms import UserProfileForm
from apps.seating.models import Seat, Seating


@login_required
def my_profile(request):
    profile = request.user.profile

    breadcrumbs = (
        (settings.SITE_NAME, '/'),
        (_(u'Profile'), reverse('myprofile')),
        (request.user.get_full_name(), ''),
    )

    return render(request, 'user/profile.html', {'quser': request.user, 
        'profile': profile, 'breadcrumbs': breadcrumbs})


@login_required
def update_profile(request):
    if request.method == 'GET':
        form = UserProfileForm(instance=request.user.profile, auto_id=True)
    else:
        form = UserProfileForm(request.POST, instance=request.user.profile, auto_id=True)
        if form.is_valid():
            form.save()
            return redirect('myprofile')
    
    breadcrumbs = (
        (settings.SITE_NAME, '/'),
        (_(u'Profile'), reverse('myprofile')),
        (_(u'Edit'), ''),
    )

    return render(request, 'user/update.html', {'form': form, 'breadcrumbs': breadcrumbs})


def user_profile(request, username):
    # Using quser for "queried user", as "user" is a reserved variable name in templates
    quser = get_object_or_404(User, username=username)
    user_seats = Seat.objects.filter(user=quser)
    # If the user is authenticated and are doing a lookup on themselves, also create
    # the form for updating and showing update information.
    if request.user.is_authenticated() and request.user == quser:
        return my_profile(request)

    profile = quser.profile
    
    breadcrumbs = (
        (settings.SITE_NAME, '/'),
        (_(u'Profile'), reverse('myprofile')),
        (quser.get_full_name(), ''),
    )
    
    return render(request, 'user/profile.html', {'quser': quser, 
        'profile': profile, 'breadcrumbs': breadcrumbs, 'user_seats': user_seats})


@login_required
def history(request):
    attended = Attendee.objects.filter(user=request.user)

    for attendee in attended:
        if attendee.lan.has_ticket(request.user):
            attendee.has_paid = True

    breadcrumbs = (
        (settings.SITE_NAME, '/'),
        (_(u'Profile'), reverse('myprofile')),
        (_(u'History'), ''),
    )

    return render(request, 'user/history.html', {'attended': attended, 'breadcrumbs': breadcrumbs})
