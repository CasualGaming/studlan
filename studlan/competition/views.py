# -*- coding: utf-8 -*-

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.template.context import RequestContext

from studlan.competition.models import Activity, Competition, Participant

def main(request):
    context = {}
    competitions = Competition.objects.all()
    competitions = shorten_descriptions(competitions, 200)

    context['activities'] = Activity.objects.all()
    context['competitions'] = competitions
    context['active'] = 'all'

    breadcrumbs = (
        ('studLAN', '/'),
        ('Competitions', ''),
    )
    context['breadcrumbs'] = breadcrumbs

    return render(request, 'competition/competitions.html', context)

def activity_details(request, activity_id):
    activity = get_object_or_404(Activity, pk=activity_id)
    
    context = {}
    competitions = Competition.objects.filter(activity=activity)
    competitions = shorten_descriptions(competitions, 200)

    context['active'] = activity.id
    context['activities'] = Activity.objects.all()
    context['competitions'] = competitions

    breadcrumbs = (
        ('studLAN', '/'),
        ('Competitions', reverse('competitions')),
        (activity, ''),
    )
    context['breadcrumbs'] = breadcrumbs

    return render(request, 'competition/competitions.html', context)

def shorten_descriptions(competitions, length):
    for c in competitions:
        if len(c.desc) > length:
            c.desc = c.desc[:length-3] + '...'
    return competitions

def competition_details(request, competition_id):
    context = {}

    competition = get_object_or_404(Competition, pk=competition_id)

    breadcrumbs = (
        ('studLAN', '/'),
        ('Competitions', reverse('competitions')),
        (competition.activity, reverse('activity_details', kwargs={'activity_id': competition.activity.id})),
        (competition, ''),
    )
    
    context['competition'] = competition
    context['breadcrumbs'] = breadcrumbs

    teams, users = competition.get_participants()

    context['teams'] = teams
    context['users'] = users
    context['participating'] = competition.has_participant(request.user)

    # Insert placeholder image if the image_url is empty
    if not competition.activity.image_url:
        competition.activity.image_url = 'http://placehold.it/150x150'

    if request.user.is_authenticated():
        owned_teams =  Team.objects.filter(leader=request.user)

        context['owned_teams'] = owned_teams
    else:
        messages.warning(request, "Please log in to register for the competition.")
    return render(request, 'competition/competition.html', context)

@login_required
def join(request, competition_id):
    competition = get_object_or_404(Competition, pk=competition_id)
    teams, users = competition.get_participants()
    
    # Checks if the user is already in the competition
    if request.user in users:
        messages.error(request, "You are already in this competition as a solo player.")
        return redirect(competition)
    for team in teams:
        if request.user == team.leader or request.user in team.members.all():
            messages.error(request, "You are already in this competition with %s." % team)
            return redirect(competition)
    
    # Checks that a form was posted, and if it contains a team id.
    if request.method == 'POST':
        team_id = request.POST.get('team')
        if team_id:
            team = get_object_or_404(Team, pk=team_id)
            participant = Participant(team=team, competition=competition)
            participant.save()
        else:
            participant = Participant(user=request.user, competition=competition)
            participant.save()
    
        messages.success(request, "You have entered %s for this competition." % participant)
    return redirect(competition)

@login_required
def leave(request, competition_id):
    competition = get_object_or_404(Competition, pk=competition_id)

    # If not participating, do nothing
    if not competition.has_participant(request.user):
        messages.error(request, "You are not participating in this competition.")
    else:
        if request.method == 'POST':
            if request.user in competition.get_users():
                participant = Participant.objects.get(user=request.user, competition=competition) 
                participant.delete()
                messages.success(request, "You are no longer participating in %s." % competition)
            else:
                was_leader = False
                for team in competition.get_teams():
                    if request.user == team.leader:
                        was_leader = True
                        participant = Participant.objects.get(team=team, competition=competition)
                        participant.delete()
                        messages.success(request, "You are have removed %s from %s." % (team, competition))
                if not was_leader:
                    messages.error(request, "You cannot remove %s from %S, you are not the team leader." % (team, competition))

    return redirect(competition)

@login_required
def forfeit(request, competition_id):
    competition = get_object_or_404(Competition, pk=competition_id)
    messages.error(request, 'Forfeit not yet implemented!')
    return redirect(competition)

# TODO
# Mode these view out of competition and into auth, 
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
