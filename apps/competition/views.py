# -*- coding: utf-8 -*-

from datetime import datetime

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import translation
from django.utils.translation import ugettext as _

from apps.competition.models import Activity, Competition, Participant
from apps.lan.models import LAN, Attendee
from apps.team.models import Team
from apps.lottery.models import Lottery


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
            (settings.SITE_NAME, '/'),
            (_(u'Competitions'), ''),
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
    context['lotteries'] = Lottery.objects.filter(lan=lan)
    
    breadcrumbs = (
        (settings.SITE_NAME, '/'),
        (_(u'Competitions'), reverse('competitions')),
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
            (settings.SITE_NAME, '/'),
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
        (settings.SITE_NAME, '/'),
        (_(u'Competitions'), reverse('competitions')),
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
        (settings.SITE_NAME, '/'),
        (_(u'Competitions'), reverse('competitions')),
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
        messages.warning(request, _(u"Please log in to register for the competition."))
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
            messages.error(request, _(u"You are already in this competition with ") + unicode(team))
            return redirect(competition)
    
    # Checks that a form was posted, and if it contains a team id
    if request.method == 'POST':
        team_id = request.POST.get('team')
        if team_id:
            team = get_object_or_404(Team, pk=team_id)

            # Check if team restrictions are in place
            if competition.enforce_team_size:
                if team.number_of_team_members() + 1 < competition.team_size:
                    messages.error(request, _(unicode(team) + u" does not have enough members (") +
                    str(team.number_of_team_members() + 1) + u"/" + str(competition.team_size) + u")")
                    return redirect(competition)

            if competition.enforce_payment:
                paid = 0
                leader_attendee = Attendee.objects.get(lan=competition.lan, user=team.leader)
                if leader_attendee.has_paid or competition.lan.has_ticket(team.leader):
                    paid += 1
                for member in team.members.all():
                    if member not in competition.lan.attendees:
                        messages.error(request, _(unicode(team) + u" has at least one member that is not signed up for "+
                        unicode(competition.lan)))
                        return redirect(competition)

                    attendee = Attendee.objects.filter(lan=competition.lan, user=member.user)
                    if attendee.has_paid or competition.lan.has_ticket(member.user):
                        paid += 1
                if paid < competition.team_size:
                    messages.error(request, _(unicode(team) + u" does not have enough members that have paid (") +
                    str(paid) + u"/" + str(competition.team_size) + u")")
                    return redirect(competition)

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
                messages.error(request, _(u"You are already in this competition as a solo player."))
                return redirect(competition)
            else:
                participant = Participant(user=request.user, competition=competition)
                participant.save()
    
        messages.success(request, _(u"You have been signed up for ") + unicode(competition))
    return redirect(competition)


@login_required
def leave(request, competition_id):
    competition = get_object_or_404(Competition, pk=competition_id)

    # If not participating, do nothing
    if not competition.has_participant(request.user):
        messages.error(request, _(u"You are not participating in this competition."))
    else:
        if request.method == 'POST':
            if request.user in competition.get_users():
                participant = Participant.objects.get(user=request.user, competition=competition) 
                participant.delete()
                messages.success(request, _(u"You are no longer participating in ") + unicode(competition))
            else:
                was_leader = False
                for team in competition.get_teams():
                    if request.user == team.leader:
                        was_leader = True
                        participant = Participant.objects.get(team=team, competition=competition)
                        participant.delete()
                        messages.success(request, _(u"You have removed ") + unicode(team) + _(u" from ") + unicode(competition))
                if not was_leader:
                    messages.error(request, "You cannot remove %s from %s, you are not the team leader." % (team, competition))

    return redirect(competition)


@login_required
def forfeit(request, competition_id):
    competition = get_object_or_404(Competition, pk=competition_id)
    messages.error(request, 'Forfeit not yet implemented!')
    return redirect(competition)


def translate_competitions(competitions):
    translated_competitions = []
    for competition in competitions:
        translated_competitions.append(competition.get_translation(language=translation.get_language()))
    return translated_competitions
