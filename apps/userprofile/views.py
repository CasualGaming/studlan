# -*- coding: utf-8 -*-

from datetime import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.translation import ugettext as _

from postman.models import Message

from apps.lan.models import Attendee
from apps.seating.models import Seat
from apps.userprofile.forms import UserProfileForm
from apps.userprofile.models import Alias, AliasType


@login_required
def my_profile(request):
    user_seats = Seat.objects.filter(user=request.user)
    profile = request.user.profile

    return render(request, 'user/profile.html', {'quser': request.user, 'profile': profile, 'user_seats': user_seats})


def user_profile(request, username):
    quser = get_object_or_404(User, username=username)
    user_seats = Seat.objects.filter(user=quser)
    profile = quser.profile

    return render(request, 'user/public_profile.html', {'quser': quser, 'profile': profile, 'user_seats': user_seats})


@login_required
def update_profile(request):
    if request.method == 'GET':
        form = UserProfileForm(instance=request.user.profile, auto_id=True)
    else:
        form = UserProfileForm(request.POST, instance=request.user.profile, auto_id=True)
        if form.is_valid():
            form.save()
            return redirect('my_profile')

    return render(request, 'user/update.html', {'form': form})


@login_required
def history(request):
    attended = Attendee.objects.filter(user=request.user)

    for attendee in attended:
        if attendee.lan.has_ticket(request.user):
            attendee.has_paid = True

    return render(request, 'user/history.html', {'attended': attended})


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

    return render(request, 'user/alias.html', {'aliases': aliases, 'alias_types': alias_types})


@login_required
def add_alias(request):
    if request.method == 'POST':
        selected_type_id = request.POST.get('selectType')
        selected_type = get_object_or_404(AliasType, pk=selected_type_id)

        alias = Alias()
        alias.user = request.user
        alias.alias_type = selected_type
        alias.nick = request.POST.get('nick')
        try:
            alias.full_clean()
        except ValidationError:
            messages.error(request, _(u'Invalid alis. Max length is 40 characters'))
            return redirect('/profile/alias')
        alias.save()
        messages.success(request, _(u'Alias was added'))

    return redirect('/profile/alias')


@login_required
def remove_alias(request, alias_id):
    alias = get_object_or_404(Alias, pk=alias_id)
    if alias.user != request.user:
        messages.error(request, _(u'You can only remove your own alias'))
        return redirect('/profile/alias')
    else:
        alias.delete()
        messages.success(request, _(u'Alias was removed'))

    return redirect('/profile/alias')
