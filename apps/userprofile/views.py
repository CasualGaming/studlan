    # -*- coding: utf-8 -*-

from datetime import datetime

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.translation import ugettext as _

from apps.lan.models import Attendee, LAN
from apps.userprofile.forms import UserProfileForm
from apps.userprofile.models import Alias, AliasType
from apps.seating.models import Seat, Seating
from postman.models import Message



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


@login_required
def user_inbox(request):
    postman_messages = Message.objects.filter(recipient=request.user).order_by('-sent_at')[:10]
    undread_messages = Message.objects.filter(recipient=request.user, read_at=None)

    for unread in undread_messages:
        unread.read_at = datetime.now()
        unread.save()

    return render(request, 'user/inbox.html', {'postman_messages': postman_messages})


@login_required
def alias(request):

    aliases = Alias.objects.filter(user=request.user)
    alias_types = AliasType.objects.all().exclude(alias__in=aliases)
    breadcrumbs = (
        (settings.SITE_NAME, '/'),
        (_(u'Profile'), reverse('myprofile')),
        (_(u'History'), ''),
    )

    return render(request, 'user/alias.html', {'aliases': aliases, 'alias_types': alias_types, 'breadcrumbs': breadcrumbs})


@login_required
def add_alias(request):
    if request.method == 'POST':
        selected_type_id = request.POST.get("selectType")
        selected_type = get_object_or_404(AliasType, pk=selected_type_id)

        alias = Alias()
        alias.user = request.user
        alias.alias_type = selected_type
        alias.nick = request.POST.get("nick")
        alias.save()
        messages.success(request, "Alias was removed")

    return redirect('/profile/alias')


@login_required
def remove_alias(request, alias_id):
    alias = get_object_or_404(Alias, pk=alias_id)
    if alias.user != request.user:
        messages.error(request, "You can only remove your own alias")
        return redirect('/profile/alias')
    else:
        alias.delete()
        messages.success(request, "Alias was removed")

    return redirect('/profile/alias')
