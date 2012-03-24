# -*- coding: utf-8 -*-

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render_to_response, render, redirect, get_object_or_404
from django.template.context import RequestContext

from studlan.team.models import Team, Member
from studlan.settings import MAX_TEAMS

def teams(request):
    teams = Team.objects.all()

    for team in teams:
        if request.user == team.leader or request.user \
            in team.members.all():
            team.is_mine = True
        else:
            team.is_mine = False

    tab = request.GET.get('tab')
    if tab is None or tab == '':
        tab = 'all'

    return render_to_response('team/teams.html', {'teams': teams,
                              'current_tab': tab},
                              context_instance=RequestContext(request))


def team(request, team_tag):
    team = get_object_or_404(Team, tag=team_tag)
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


def add_member(request, team_tag):
    if request.method == 'POST':
        team = get_object_or_404(Team, tag=team_tag)
        if request.user != team.leader:
            messages.error(request, "You are not the team leader, you cannot remove team members.")
        else:
            uid = request.POST.get('selectMember')
            user = get_object_or_404(User, pk=uid)
            
            member = Member()
            member.team = team
            member.user = user
            member.save()

            messages.success(request, 'User %s added.' % user.username)

    return redirect('team', team_tag=team_tag)


def remove_member(request, team_tag, user_id):
    team = get_object_or_404(Team, tag=team_tag)
    if request.user != team.leader:
        messages.error(request, "You are not the team leader, you cannot remove team members.")
    else:
        user = User.objects.get(id = user_id)
        member = get_object_or_404(Member, user=user)
        member.delete()
        messages.success(request, 'User %s removed.' % user.username)

    return redirect('team', team_tag=team_tag)


def create_team(request):
    if Team.objects.filter(leader=request.user).count() >= MAX_TEAMS:
        messages.error(request, "You cannot be leader of more than %i teams." % MAX_TEAMS)
        return redirect('teams')
    else:
        team = Team()
        team.leader = request.user
        team.title = request.POST.get('title')
        team.tag = request.POST.get('tag')
        team.save()

        messages.success(request, 'Team %s has been created.' % team.title)
        
        return redirect('team', team_tag=team.tag)
