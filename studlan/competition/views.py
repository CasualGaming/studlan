#!/usr/bin/python
# -*- coding: utf-8 -*-

from studlan.competition.models import Activity, Competition, Team
from django.shortcuts import render_to_response, redirect, \
    get_object_or_404
from django.template.context import RequestContext
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages


def main(request):
    competitions = Competition.objects.all()
    activities = Activity.objects.all()

    for c in competitions:
        if len(c.desc) >= 200:
            c.desc = c.desc[:197] + '...'

    tab = request.GET.get('tab')
    if tab is None or tab == '':
        tab = 'all'

    return render_to_response('competitions.html',
                              {'competitions': competitions,
                              'activities': activities,
                              'current_tab': tab},
                              context_instance=RequestContext(request))


def single(request, competition_id):
    competition = get_object_or_404(Competition, pk=competition_id)

    if not 'http' in competition.activity.image_url:
        competition.activity.image_url = 'http://placehold.it/150x150'

    if request.user.is_authenticated():
        leader_of_teams = Team.objects.filter(leader=request.user)

        teams_in_competition = []
        teams_not_in_competition = []

        for x in leader_of_teams:
            if x in competition.teams.all():
                teams_in_competition.append(x)
            else:
                teams_not_in_competition.append(x)

        has_teams_in_competition = len(teams_in_competition) > 0
        has_teams_not_in_competition = (len(teams_not_in_competition) > 0) and not has_teams_in_competition
        is_leader = len(leader_of_teams) > 0

        return render_to_response('competition.html', {
            'competition': competition,
            'is_leader': is_leader,
            'has_teams_in_competition': has_teams_in_competition,
            'has_teams_not_in_competition': has_teams_not_in_competition,
            'teams_in_competition': teams_in_competition,
            'teams_not_in_competition': teams_not_in_competition,
            }, context_instance=RequestContext(request))
    else:

        return render_to_response('competition.html',
                                  {'competition': competition},
                                  context_instance=RequestContext(request))


def teams(request):
    teams = Team.objects.all()
    competitions = Competition.objects.all()

    for team in teams:
        if request.user == team.leader or request.user in team.members.all():
            team.is_mine = True
        else:
            team.is_mine = False

    tab = request.GET.get('tab')
    if tab is None or tab == '':
        tab = 'all'

    return render_to_response('teams.html', {'teams': teams,
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

    return render_to_response(  'team.html', {
                                'team': team,
                                'users': users2},
                                context_instance=RequestContext(request))

def add_member(request, team_tag):
    team = get_object_or_404(Team, tag=team_tag)
    uid = request.POST.get("selectMember")
    user = User.objects.get(pk=uid)
    #user = get_object_or_404(User, username=username)
    team.members.add(user)
    team.save()
    messages.add_message(request, messages.SUCCESS,
                        'User %s added.' % user.username)
    #return redirect('team', team_tag=team_tag)
    return redirect('team', team_tag=team_tag)

def create_team(request):
    team = Team()
    team.leader = request.user
    team.title = request.POST.get('title')
    team.tag = request.POST.get('tag')
    messages.add_message(request, messages.SUCCESS,
                         'Team %s has been created.' % team.title)
    team.save()

    return redirect('teams')


def join(request, competition_id):
    competition = get_object_or_404(Competition, pk=competition_id)
    competition.participants.add(request.user)
    messages.add_message(request, messages.WARNING,
                         'You\'re now participating in %s.'
                         % competition.title)
    return redirect('competition', competition_id=competition_id)


def leave(request, competition_id):
    competition = get_object_or_404(Competition, pk=competition_id)
    competition.participants.remove(request.user)
    messages.add_message(request, messages.WARNING,
                         'You\'re no longer participating in %s.'
                         % competition.title)
    return redirect('competition', competition_id=competition_id)


def forfeit(request, competition_id):
    competition = get_object_or_404(Competition, pk=competition_id)
    messages.add_message(request, messages.ERROR,
                         'Forfeit not yet implemented!')
    return redirect('competition', competition_id=competition_id)


def join_team(request, competition_id):
    competition = get_object_or_404(Competition, pk=competition_id)
    num = request.POST['team']
    team = Team.objects.filter(id=int(num))
    competition.teams.add(int(num))
    messages.add_message(request, messages.SUCCESS,
                         "You're now participating in %s with the team."
                          % competition.title)
    return redirect('competition', competition_id=competition_id)


def leave_team(request, competition_id):
    competition = get_object_or_404(Competition, pk=competition_id)
    num = request.POST['team']
    competition.teams.remove(int(num))
    messages.add_message(request, messages.WARNING,
                         "You're no longer participating in %s with "
                         "the team." % competition.title)
    return redirect('competition', competition_id=competition_id)


def forfeit_team(request, competition_id):
    competition = get_object_or_404(Competition, pk=competition_id)
    messages.add_message(request, messages.ERROR,
                         'Forfeit not yet implemented!')
    return redirect('competition', competition_id=competition_id)


def log_in(request):
    username = password = ''
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                messages.add_message(request, messages.SUCCESS,
                        'You\'ve successfully logged in.')
            else:
                messages.add_message(request, messages.WARNING,
                        'Your account is not active, please try again '
                        'or contact the site admin if the problem '
                        'persists.')
        else:

            messages.add_message(request, messages.ERROR,
                                 'Wrong username/password.')
    return redirect('news')


def log_out(request):
    logout(request)

    messages.add_message(request, messages.SUCCESS,
                         'You\'ve successfully logged out.')
    return redirect('news')


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
                                 'Registration '
                                 'successful. You may now log '
                                 'in.')

    return redirect('news')
