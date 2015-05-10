# -*- coding: utf-8 -*-

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.template.context import RequestContext
from django.utils.translation import ugettext as _

from apps.misc.forms import InlineSpanErrorList
from apps.team.models import Team, Member, Invitation
from apps.team.forms import TeamCreationForm

from postman.api import pm_write
import uuid


def teams(request):
    teams = Team.objects.all()

    breadcrumbs = (
        (settings.SITE_NAME, '/'),
        (_(u'Teams'), ''),
    )

    return render(request, 'team/teams.html', {'teams': teams, 'breadcrumbs': breadcrumbs})


@login_required
def my_teams(request):
    teams = Team.objects.filter(Q(leader=request.user) | Q(members=request.user)).distinct()

    breadcrumbs = (
        (settings.SITE_NAME, '/'),
        (_(u'Teams'), reverse('teams')),
        (_(u'My teams'), ''),
    )

    return render(request, 'team/my_teams.html', {'teams': teams, 'breadcrumbs': breadcrumbs})

@login_required
def create_team(request):
    if request.method == 'POST':
        # Stop if a person tries to create more than the allowed ammount of teams.        
        if Team.objects.filter(leader=request.user).count() >= settings.MAX_TEAMS:
            messages.error(request, _(u"You cannot be leader of more than ") + settings.MAX_TEAMS + _(u" teams."))  
            return redirect('teams')

        form = TeamCreationForm(request.POST)
        if form.is_valid():
            cleaned = form.cleaned_data

            team = Team(
                leader = request.user,
                title = cleaned['title'],
                tag = cleaned['tag'],
            )
            team.save()

            messages.success(request, unicode(team) + _(u" has been created."))
            return redirect(team)
        else:
            form = TeamCreationForm(request.POST, auto_id=True, error_class=InlineSpanErrorList) 
    else:
        form = TeamCreationForm()

    breadcrumbs = (
        (settings.SITE_NAME, '/'),
        (_(u'Teams'), reverse('teams')),
        (_(u'Create team'), ''),
    )

    return render(request, 'team/create_team.html', {'breadcrumbs': breadcrumbs, 'form': form})


@login_required
def disband_team(request, team_id):
    team = get_object_or_404(Team, pk=team_id)
    if request.user != team.leader:
        messages.error(request, _(u"You can only disband teams that you are leader of."))
        return redirect(team)
    else:
        team.delete()

        messages.success(request, unicode(team) + _(u" was successfully deleted."))
        return redirect('teams')


def show_team(request, team_id):
    team = get_object_or_404(Team, pk=team_id)
    if request.user == team.leader:
        team.is_mine = True
    else:
        team.is_mine = False

    users = User.objects.all()
    users2 = []
    for user in users:
        if user != team.leader:
            if user not in team.members.all():
                users2.append(user)

    users2.sort(key=lambda x: x.username.lower(), reverse=False)
    
    breadcrumbs = (
        (settings.SITE_NAME, '/'),
        (_(u'Teams'), reverse('teams')),
        (team, ''),
    )

    return render(request, 'team/team.html', {'team': team, 'users': users2, 'breadcrumbs': breadcrumbs})


@login_required
def add_member(request, team_id):
    if request.method == 'POST':
        team = get_object_or_404(Team, pk=team_id)
        if request.user != team.leader:
            messages.error(request, _(u"You are not the team leader, you cannot add team members."))
        else:
            user_id = request.POST.get("selectMember")
            user = get_object_or_404(User, pk=user_id)
            if len(Member.objects.filter(user=user, team=team)) > 0:
                messages.error(request, unicode(user) + _(u" is already on your team."))
            else:
                member = Member()
                member.team = team
                member.user = user
                member.save()

                messages.success(request, unicode(user) + _(u' was added to your team'))

    return redirect(team)


@login_required
def invite_member(request, team_id):
    if request.method == 'POST':
        team = get_object_or_404(Team, pk=team_id)
        if request.user != team.leader:
            messages.error(request, _(u"You are not the team leader, you cannot add team members."))
        else:
            user_id = request.POST.get("selectMember")
            user = get_object_or_404(User, pk=user_id)
            if len(Member.objects.filter(user=user, team=team)) > 0:
                messages.error(request, unicode(user) + _(u" is already on your team."))
            else:
                invitation = Invitation()
                invitation.team = team
                invitation.invitee = user
                invitation.team_leader = request.user
                invitation.token = uuid.uuid1().hex
                invitation.save()
                pm_write(request.user, user, 'Team invitation', body='You have been invited to ' + team.title + ' by '
                         + str(request.user) + '. To accept the invitation, click this link: http://' + request.META['HTTP_HOST']
                         + team.get_absolute_url())

                messages.success(request, unicode(user) + _(u' was invited to your team'))

    return redirect(team)


@login_required
def join_team(request, team_id):
    if request.method == 'POST':
        team = get_object_or_404(Team, pk=team_id)
        if request.user != team.leader:
            messages.error(request, _(u"You are not the team leader, you cannot add team members."))
        else:
            user_id = request.POST.get("selectMember")
            user = get_object_or_404(User, pk=user_id)
            if len(Member.objects.filter(user=user, team=team)) > 0:
                messages.error(request, unicode(user) + _(u" is already on your team."))
            else:
                member = Member()
                member.team = team
                member.user = user
                member.save()

                messages.success(request, unicode(user) + _(u' was added to your team'))

    return redirect(team)




@login_required
def remove_member(request, team_id, user_id):
    team = get_object_or_404(Team, pk=team_id)
    user = get_object_or_404(User, pk=user_id)
    if request.user != team.leader and request.user != user:
        messages.error(request, _(u"You are not the team leader, you cannot remove other team members."))
    else:
        member = get_object_or_404(Member, user=user, team=team)
        member.delete()
        if request.user == user:
            messages.success(request, _(u'You have left team ') + unicode(team))
        else:
            messages.success(request, unicode(user.username) + _(u" removed from your team."))

    return redirect(team)
