# -*- coding: utf-8 -*-

import uuid

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.utils.translation import ugettext as _
from django.views.decorators.http import require_POST, require_safe

from postman.api import pm_write
from postman.models import Message

from apps.misc.forms import InlineSpanErrorList
from apps.team.forms import TeamCreationForm
from apps.team.models import Invitation, Member, Team


@require_safe
def teams(request):
    teams = Team.objects.all()
    return render(request, 'team/teams.html', {'teams': teams})


@require_safe
def show_team(request, team_id):
    team = get_object_or_404(Team, pk=team_id)
    invitations = Invitation.objects.filter(team=team)
    authenticated = request.user.is_authenticated()

    context = {
        'team': team,
        'is_leader': request.user == team.leader,
        'is_normal_member': team.member_set.filter(user=request.user).exists() if authenticated else None,
        'invitations': invitations,
        'my_invitation': invitations.filter(invitee=request.user) if authenticated else None,
    }

    return render(request, 'team/team.html', context)


@require_safe
@login_required
def my_teams(request):
    teams = Team.objects.filter(Q(leader=request.user) | Q(members=request.user)).distinct()
    return render(request, 'team/my_teams.html', {'teams': teams})


@login_required
def create_team(request):
    if request.method != 'POST':
        return render(request, 'team/create_team.html', {'form': TeamCreationForm()})

    # Stop if a person tries to create more than the allowed ammount of teams.
    if Team.objects.filter(leader=request.user).count() >= settings.MAX_TEAMS:
        messages.error(request, _(u'You can\'t be the leader of more than {max} teams.').format(max=settings.MAX_TEAMS))
        return redirect('teams')

    form = TeamCreationForm(request.POST)
    if form.is_valid():
        cleaned = form.cleaned_data
        team = Team(
            leader=request.user,
            title=cleaned['title'],
            tag=cleaned['tag'],
        )
        team.save()
        messages.success(request, _(u'Team {team} has been created.').format(team=team))
        return redirect(team)
    else:
        # Return with errors
        form = TeamCreationForm(request.POST, auto_id=True, error_class=InlineSpanErrorList)
        return render(request, 'team/create_team.html', {'form': form})


@require_POST
@login_required
def disband_team(request, team_id):
    team = get_object_or_404(Team, pk=team_id)
    if request.user != team.leader:
        messages.error(request, _(u'Only the team leader may disband the team.'))
        return redirect(team)

    # Delete all invite messages
    for invitation in Invitation.objects.filter(team=team):
        Message.objects.filter(subject=invitation.token).delete()

    # Members and invitations are deleted by cascade
    team.delete()
    messages.success(request, _(u'Team {team} was deleted.').format(team=team))
    return redirect('teams')


@require_POST
@login_required
def invite_member(request, team_id):
    team = get_object_or_404(Team, pk=team_id)

    if request.user != team.leader:
        messages.error(request, _(u'Only the team leader may invite members.'))
        return redirect(team)

    username = request.POST.get('user')
    if not username:
        messages.error(request, _(u'No username was specified.'))
        return redirect(team)
    elif username == request.user.username:
        messages.error(request, _(u'You can\'t invite yourself.'))
        return redirect(team)

    user_qs = User.objects.filter(username=username)
    if not user_qs.exists():
        messages.error(request, _(u'User {user} was not found.').format(user=username))
        return redirect(team)
    user = user_qs[0]

    if Member.objects.filter(team=team, user=user).exists():
        messages.error(request, _(u'User {user} is already on the team.').format(user=user))
        return redirect(team)

    if Invitation.objects.filter(team=team, invitee=user).exists():
        messages.error(request, _(u'User {user} is already invited to the team.').format(user=user))
        return redirect(team)

    invitation = Invitation()
    invitation.team = team
    invitation.invitee = user
    invitation.token = uuid.uuid1().hex
    invitation.save()

    context = {
        'team': team,
        'inviter': request.user,
    }
    message = render_to_string('team/message/team_invitation.html', context, request).strip()
    pm_write(request.user, user, invitation.token, body=message)

    messages.success(request, _(u'User {user} was invited to the team.').format(user=user))
    return redirect(team)


@require_POST
@login_required
def uninvite_member(request, team_id):
    # Weird cases:
    # - Team leaders may uninvite themselves
    # - Members may be uninvited (no effect)

    team = get_object_or_404(Team, pk=team_id)

    if request.user != team.leader:
        messages.error(request, _(u'Only the team leader may uninvite members.'))
        return redirect(team)

    username = request.POST.get('user')
    if not username:
        messages.error(request, _(u'No username was specified.'))
        return redirect(team)

    user_qs = User.objects.filter(username=username)
    if not user_qs.exists():
        messages.error(request, _(u'User {user} was not found.').format(user=username))
        return redirect(team)
    user = user_qs[0]

    invitation_qs = Invitation.objects.filter(team=team, invitee=user)
    if not invitation_qs.exists():
        messages.error(request, _(u'User {user} is not invited to the team.').format(user=user))
        return redirect(team)
    invitation = invitation_qs[0]

    # Delete both invitation and message
    Message.objects.filter(subject=invitation.token).delete()
    invitation.delete()

    messages.success(request, _(u'User {user} was uninvited to the team.').format(user=user))
    return redirect(team)


@require_POST
@login_required
def accept_member_invite(request, team_id):
    team = get_object_or_404(Team, pk=team_id)
    user = request.user

    if request.user == team.leader:
        messages.error(request, _(u'You are already the team leader of team {team}.').format(team=team))
        return redirect(team)

    if Member.objects.filter(team=team, user=user).exists():
        messages.error(request, _(u'You are already on team {team}.').format(user=user, team=team))
        return redirect(team)

    invitation_qs = Invitation.objects.filter(team=team, invitee=user)
    if not invitation_qs.exists():
        messages.error(request, _(u'You are not invited to team {team}.').format(user=user, team=team))
        return redirect(team)
    invitation = invitation_qs[0]

    member = Member()
    member.team = team
    member.user = user
    member.save()

    # Delete both invitation and message
    Message.objects.filter(subject=invitation.token).delete()
    invitation.delete()

    messages.success(request, _(u'You have accepted the membership invitation from team {team}.').format(team=team))
    return redirect(team)


@require_POST
@login_required
def decline_member_invite(request, team_id):
    # Weird case: Team leaders and members may decline extra invites

    team = get_object_or_404(Team, pk=team_id)
    user = request.user

    invitation_qs = Invitation.objects.filter(team=team, invitee=user)
    if not invitation_qs.exists():
        messages.error(request, _(u'You are not invited to team {team}.').format(user=user, team=team))
        return redirect(team)
    invitation = invitation_qs[0]

    # Delete both invitation and message
    Message.objects.filter(subject=invitation.token).delete()
    invitation.delete()

    messages.success(request, _(u'You have declined the membership invitation from team {team}.').format(team=team))
    return redirect(team)


@require_POST
@login_required
def kick_member(request, team_id):
    team = get_object_or_404(Team, pk=team_id)

    if request.user != team.leader:
        messages.error(request, _(u'Only the team leader may kick members.'))
        return redirect(team)

    username = request.POST.get('user')
    if not username:
        messages.error(request, _(u'No username was specified.'))
        return redirect(team)
    elif username == request.user.username:
        messages.error(request, _(u'You can\'t kick yourself.'))
        return redirect(team)

    user_qs = User.objects.filter(username=username)
    if not user_qs.exists():
        messages.error(request, _(u'User {user} was not found.').format(user=username))
        return redirect(team)
    user = user_qs[0]

    member_qs = Member.objects.filter(team=team, user=user)
    if not member_qs.exists():
        messages.error(request, _(u'User {user} is not a member of the team.').format(user=user))
        return redirect(team)
    member = member_qs[0]

    member.delete()
    messages.success(request, _(u'{user} was kicked from the team.').format(user=member.user))
    return redirect(team)


@require_POST
@login_required
def leave_team(request, team_id):
    team = get_object_or_404(Team, pk=team_id)

    if request.user == team.leader:
        messages.error(request, _(u'You are the team leader, the only way to leave the team is to disband it.'))
        return redirect(team)

    member_qs = Member.objects.filter(team=team, user=request.user)
    if not member_qs.exists():
        messages.error(request, _(u'You are not a member of this team.'))
        return redirect(team)

    member = member_qs[0]
    member.delete()
    messages.success(request, _(u'You have left team {team}.').format(team=team))
    return redirect(team)
