# -*- coding: utf-8 -*-

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import render_to_response, render, redirect, get_object_or_404
from django.template.context import RequestContext

from studlan.team.models import Team, Member
from studlan.settings import MAX_TEAMS

def teams(request):
    teams = Team.objects.all()
    return render(request, 'team/teams.html', {'teams': teams})

@login_required
def my_teams(request):
    teams = Team.objects.filter(Q(leader=request.user) | Q(members=request.user))
    return render(request, 'team/my_teams.html', {'teams': teams})

@login_required
def create_team(request):
    if request.method == 'POST':
        if Team.objects.filter(leader=request.user).count() >= MAX_TEAMS:
            messages.error(request, "You cannot be leader of more than %i teams." % MAX_TEAMS)
            return redirect('teams')
        else:
            team = Team()
            team.leader = request.user
            team.title = request.POST.get('title')
            team.tag = request.POST.get('tag')
            team.save()

            messages.success(request, 'Team %s has been created.' % team)
            return redirect(team)
    else:
        return render(request, 'team/create_team.html', {})

def disband_team(request, team_id):
    team = get_object_or_404(Team, pk=team_id)
    if request.user != team.leader:
        messages.error(request, "You can only disband teams that you are leader of.")
        return redirect(team)
    else:
        team.delete()

        messages.success(request, "Team %s was successfully deleted." % team)
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

    return render_to_response('team/team.html', {'team': team,
                              'users': users2},
                              context_instance=RequestContext(request))


def add_member(request, team_id):
    if request.method == 'POST':
        team = get_object_or_404(Team, pk=team_id)
        if request.user != team.leader:
            messages.error(request, "You are not the team leader, you cannot remove team members.")
        else:
            user_id = request.POST.get('selectMember')
            user = get_object_or_404(User, pk=user_id)
            if len(Member.objects.filter(user=user, team=team)) > 0:
                messages.error(request, "%s is already on your team." % user)
            else:
                member = Member()
                member.team = team
                member.user = user
                member.save()

                messages.success(request, 'User %s added.' % user.username)

    return redirect(team)


def remove_member(request, team_id, user_id):
    team = get_object_or_404(Team, pk=team_id)
    user = get_object_or_404(User, pk=user_id)
    if request.user != team.leader and request.user != user:
        messages.error(request, "You are not the team leader, you cannot remove other team members.")
    else:
        member = get_object_or_404(Member, user=user, team=team)
        member.delete()
        if request.user == user:
            messages.success(request, 'You have left team %s.' % team)
        else:
            messages.success(request, 'User %s removed.' % user.username)

    return redirect(team)
