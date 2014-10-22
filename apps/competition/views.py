# -*- coding: utf-8 -*-

from datetime import datetime

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.template.context import RequestContext
from django.utils import translation

from apps.competition.models import Activity, Competition, Participant
from apps.lan.models import LAN
from apps.team.models import Team

def main(request):
    lans = LAN.objects.filter(end_date__gte=datetime.now())
    if lans:
        next_lan = lans[0]
        return redirect('competitions_show_lan', lan_id=next_lan.id)
    else:
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

def main_filtered(request, lan_id):
    lan = get_object_or_404(LAN, pk=lan_id)

    context = {}
    competitions = Competition.objects.filter(lan=lan)
    competitions = shorten_descriptions(competitions, 200)

    context['activities'] = Activity.objects.all()
    context['competitions'] = competitions
    context['active'] = 'all'
    context['lan'] = lan
    
    breadcrumbs = (
        ('studLAN', '/'),
        ('Competitions', reverse('competitions')),
        (lan, '')
    )
    context['breadcrumbs'] = breadcrumbs

    return render(request, 'competition/competitions.html', context)

def activity_details(request, activity_id):
    lans = LAN.objects.filter(end_date__gte=datetime.now())
    if lans:
        next_lan = lans[0]
        return redirect('activity_details_show_lan', lan_id=next_lan.id, activity_id=activity_id)
    else:
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

def activity_details_filtered(request, lan_id, activity_id):
    lan = get_object_or_404(LAN, pk=lan_id)
    activity = get_object_or_404(Activity, pk=activity_id)

    context = {}
    competitions = Competition.objects.filter(lan=lan, activity=activity)
    competitions = shorten_descriptions(competitions, 200)

    context['active'] = activity.id
    context['activities'] = Activity.objects.all()
    context['competitions'] = competitions
    context['lan'] = lan

    breadcrumbs = (
        ('studLAN', '/'),
        ('Competitions', reverse('competitions')),
        (lan, reverse('lan_details', kwargs={'lan_id': lan.id})),
        (activity, ''),
    )
    context['breadcrumbs'] = breadcrumbs

    return render(request, 'competition/competitions.html', context)

def shorten_descriptions(competitions, length):
    for c in competitions:
        if len(c.get_translation().translated_description) > length:
            c.get_translation().translated_description = c.get_translation().translated_description[:length-3] + '...'
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
    
    context['breadcrumbs'] = breadcrumbs

    teams, users = competition.get_participants()

    context['teams'] = teams
    context['users'] = users

    if competition.has_participant(request.user):
        if request.user in users:
            context['participating'] = 'solo'
        else:
            context['participating'] = 'team'

    # Insert placeholder image if the image_url is empty
    if not competition.activity.image_url:
        competition.activity.image_url = 'http://placehold.it/150x150'

    if request.user.is_authenticated():
        owned_teams =  Team.objects.filter(leader=request.user)

        context['owned_teams'] = owned_teams
    else:
        messages.warning(request, "Please log in to register for the competition.")
    context['competition'] = competition
    return render(request, 'competition/competition.html', context)

@login_required
def join(request, competition_id):
    competition = get_object_or_404(Competition, pk=competition_id)
    teams, users = competition.get_participants()
    
    # Checks if the user is already in the competition with a team, solo queue should be
    # overridden by team signup, but not other way around
    for team in teams:
        if request.user == team.leader or request.user in team.members.all():
            messages.error(request, "You are already in this competition with %s." % team)
            return redirect(competition)
    
    # Checks that a form was posted, and if it contains a team id
    if request.method == 'POST':
        team_id = request.POST.get('team')
        if team_id:
            team = get_object_or_404(Team, pk=team_id)
           
            # Go through all members of the team and delete their individual participation entries 
            if request.user in users:
                participant = Participant.objects.get(user=request.user, competition=competition)
                participant.delete()
            
            members = team.members.all()
            participants = Participant.objects.filter(user__in=members)
            
            for participant in participants:
                participant.delete()

            # Add the team
            participant = Participant(team=team, competition=competition)
            participant.save()

        else:
            # If solo signup and already signed
            if request.user in users:
                messages.error(request, "You are already in this competition as a solo player.")
                return redirect(competition)
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
                    messages.error(request, "You cannot remove %s from %s, you are not the team leader." % (team, competition))

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
    
def translate_competitions(competitions):
    translated_competitions = []
    for competition in competitions:
        translated_competitions.append(competition.get_translation(language=translation.get_language()))
    return translated_competitions
