# -*- coding: utf-8 -*-

from datetime import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.translation import ugettext as _
from django.views.decorators.http import require_POST, require_safe

from postman.models import Message

from apps.competition.models import Competition
from apps.lan.models import Attendee
from apps.userprofile.forms import UserProfileForm
from apps.userprofile.models import Alias, AliasType


@require_safe
@login_required
def my_profile(request):
    context = {}
    quser = request.user
    context['quser'] = quser
    context['profile'] = quser.profile

    return render(request, 'user/profile.html', context)


@require_safe
def user_profile(request, username):
    context = {}
    quser = get_object_or_404(User, username=username)
    context['quser'] = quser
    context['profile'] = quser.profile
    if request.user == quser or request.user.has_perm('userprofile.show_private_info'):
        attendances = Attendee.objects.filter(user=quser)
        competitions = Competition.get_all_for_user(quser)
        context['attendances'] = attendances
        context['competitions'] = competitions

    return render(request, 'user/public_profile.html', context)


@require_safe
@login_required
def user_competitions(request):
    competitions = Competition.get_all_for_user(request.user)
    return render(request, 'user/competitions.html', {'competitions': competitions})


@login_required
def update_profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user.profile, auto_id=True)
        if form.is_valid():
            form.save()
            return redirect('my_profile')
    else:
        form = UserProfileForm(instance=request.user.profile, auto_id=True)
    return render(request, 'user/update.html', {'form': form})


@require_safe
@login_required
def history(request):
    attendances = Attendee.objects.filter(user=request.user)
    return render(request, 'user/history.html', {'attendances': attendances})


@require_safe
@login_required
def user_inbox(request):
    postman_messages = Message.objects.filter(recipient=request.user).order_by('-sent_at')[:10]
    undread_messages = Message.objects.filter(recipient=request.user, read_at=None)

    for unread in undread_messages:
        unread.read_at = datetime.now()
        unread.save()

    return render(request, 'user/inbox.html', {'postman_messages': postman_messages})


@require_safe
@login_required
def alias(request):
    aliases = Alias.objects.filter(user=request.user)
    alias_types = AliasType.objects.all().exclude(alias__in=aliases)

    return render(request, 'user/alias.html', {'aliases': aliases, 'alias_types': alias_types})


@require_POST
@login_required
def add_alias(request):
    selected_type_id = request.POST.get('selectType')
    selected_type = get_object_or_404(AliasType, pk=selected_type_id)

    alias = Alias()
    alias.user = request.user
    alias.alias_type = selected_type
    alias.nick = request.POST.get('nick')
    try:
        alias.full_clean()
    except ValidationError:
        messages.error(request, _(u'Invalid alias. Max length is 40 characters.'))
        return redirect('/profile/alias')
    alias.save()
    messages.success(request, _(u'The alias was added.'))

    return redirect('/profile/alias')


@require_POST
@login_required
def remove_alias(request, alias_id):
    alias = get_object_or_404(Alias, pk=alias_id)

    if alias.user != request.user:
        messages.error(request, _(u'You can only remove your own aliases.'))
        return redirect('/profile/alias')

    alias.delete()
    messages.success(request, _(u'The alias was removed.'))

    return redirect('/profile/alias')
