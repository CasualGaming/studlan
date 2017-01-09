# -*- coding: utf-8 -*-

from datetime import datetime
import challonge
from django.contrib.admin.views.decorators import staff_member_required
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.contrib.auth.models import User
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import translation
from django.utils.translation import ugettext as _

from apps.competition.models import Activity, Competition, Participant, Match
from apps.lan.models import LAN, Attendee
from apps.team.models import Team
from apps.lottery.models import Lottery
import re


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
    challonge.set_credentials(settings.CHALLONGE_API_USERNAME, settings.CHALLONGE_API_KEY)

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
        p = None
        if request.user in users:
            context['participating'] = 'solo'
            p = Participant.objects.get(user=request.user, competition=competition)

        else:
            context['participating'] = 'team'
            owned_teams = Team.objects.filter(leader=request.user)
            k = set(owned_teams) & set(teams)
            if k:
                p = Participant.objects.get(team=k.pop(), competition=competition)
        if p:
            try:
                match = Match.objects.get((Q(player1=p) | Q(player2=p)) & Q(state='open'))
                context['player_match'] = match
                context['point_choices'] = range(0, competition.max_match_points + 1)
                if match.player1 == p:
                    context['player'] = 1
                    if match.p1_reg_score:
                        context['registered'] = True
                    else:
                        context['registered'] = False
                else:
                    context['player'] = 2
                    if match.p2_reg_score:
                        context['registered'] = True
                    else:
                        context['registered'] = False
            except ObjectDoesNotExist:
                if 1 < competition.status < 4:
                    messages.warning(request, 'You have no current match, please check the brackets for more information')

    # Insert placeholder image if the image_url is empty
    if not competition.activity.image_url:
        competition.activity.image_url = 'http://placehold.it/150x150'

    if request.user.is_authenticated():
        owned_teams =  Team.objects.filter(leader=request.user)

        context['owned_teams'] = owned_teams
    else:
        messages.warning(request, _(u"Please log in to register for the competition."))
    context['competition'] = competition



    #admin control panel
    if request.user.is_staff and competition.status > 1 and competition.challonge_url:
        context['open_matches'] = Match.objects.filter(Q(competition=competition, state='open') | Q(competition=competition, state='error'))
    return render(request, 'competition/competition.html', context)


def update_match_list(competition):
    challonge.set_credentials(settings.CHALLONGE_API_USERNAME, settings.CHALLONGE_API_KEY)
    c_open_matches = challonge.matches.index(competition.challonge_url)
    competition_matches = Match.objects.filter(competition=competition)
    for copen in c_open_matches:
        if competition_matches:
            open_match = Match.objects.get(matchid=str(copen['id']), competition=competition)
        else:
            open_match = Match(matchid=str(copen['id']), competition=competition)
        if open_match.state != 'error':
            open_match.state = copen['state']
        if copen['player1_id']:
            open_match.player1 = Participant.objects.get(competition=competition, cid=copen['player1_id'])
        if copen['player2_id']:
            open_match.player2 = Participant.objects.get(competition=competition, cid=copen['player2_id'])
        open_match.save()
    return Match.objects.filter(competition=competition, state='open')


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

            # Check if team size restrictions are in place
            if competition.enforce_team_size:
                if team.number_of_team_members() + 1 < competition.team_size:
                    messages.error(request, _(unicode(team) + u" does not have enough members (") +
                    str(team.number_of_team_members() + 1) + u"/" + str(competition.team_size) + u")")
                    return redirect(competition)

            # Check if payment restrictions are in place
            if competition.enforce_payment:
                if team.number_of_attending_members(competition.lan) < team.number_of_team_members() + 1:
                    messages.error(request, _(unicode(team) + u" has at least one member that is not signed up for "+
                        unicode(competition.lan)))
                    return redirect(competition)
                else:
                    if team.number_of_paid_members(competition.lan) < competition.team_size:
                        messages.error(request, _(unicode(team) + u" does not have enough members that have paid (") +
                        unicode(team.number_of_paid_members(competition.lan)) + u"/" + str(competition.team_size) + u")")
                        return redirect(competition)

            # Check if alias restrictions are in place
            if competition.require_alias:
                if team.number_of_aliases(competition) < team.number_of_team_members() + 1:
                    if team.number_of_team_members() + 1 - team.number_of_aliases(competition) < 4:
                        messages.error(request, _(u"Several members of " + unicode(team) + u" are missing aliases for " +
                                   unicode(competition)))
                        for member in team.members.all():
                            if not competition.has_alias(member):
                                messages.error(request, _(unicode(member) + u" is missing an alias for ") +
                                   unicode(competition))
                        if not competition.has_alias(team.leader):
                            messages.error(request, _(unicode(team.leader) + u" is missing an alias for ") +
                                   unicode(competition))
                    else:
                        messages.error(request, _(u"Several members of " + unicode(team) + u" are missing aliases for ") +
                                   unicode(competition))
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
                if competition.require_alias:
                    if not competition.has_alias(request.user):
                        messages.error(request, _(u"You do not have the required alias."))
                        return redirect(competition)
                    participant = Participant(user=request.user, competition=competition)
                    participant.save()
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


@staff_member_required
@login_required
def start_compo(request, competition_id):
    competition = get_object_or_404(Competition, pk=competition_id)
    if competition.status == 1:
        try:
            names = []
            teams, users = competition.get_participants()
            if competition.use_teams:
                for team in teams:
                    names.append(team.title)

            else:
                for user in users:
                    names.append(user.username)

            if len(names) < 2:
                messages.error(request, 'Too few participants')
                return redirect(competition)

            if competition.tournament_format is None:
                messages.error(request, 'Set competition tournament format before using this feature')
                return redirect(competition)

            url = unicode(competition.lan) + unicode(competition.activity)
            url = re.sub('[^0-9a-zA-Z]+', '', url)
            challonge.set_credentials(settings.CHALLONGE_API_USERNAME, settings.CHALLONGE_API_KEY)
            challonge.tournaments.create(competition.activity.title, url, tournament_type=competition.tournament_format)
            challonge.participants.bulk_add(url, names)
            challonge.tournaments.start(url)
            cparticipants = challonge.participants.index(url)

            for part in cparticipants:
                if not competition.use_teams:
                    par = Participant.objects.get(user__username=part['name'], competition=competition)
                else:
                    par = Participant.objects.get(team__title=part['name'], competition=competition)
                par.cid = part['id']
                par.save()

            competition.status = 3
            competition.challonge_url = url
            competition.save()
            update_match_list(competition)
            messages.success(request, 'Tournament has started!')
        except:
            messages.error(request, 'Something went wrong')

    return redirect(competition)


@login_required
def register_score(request, competition_id, match_id, player_id):
    competition = get_object_or_404(Competition, pk=competition_id)
    match = get_object_or_404(Match, id=match_id, competition=competition)
    if request.method == 'POST':
        max_score = competition.max_match_points
        p1_score = request.POST.get('player1score')
        p2_score = request.POST.get('player2score')

        if int(p1_score) > max_score or int(p1_score) < 0 or int(p2_score) > max_score or int(p2_score) < 0:
            messages.error(request, 'Invalid score. Score must be > 0 and < ' + unicode(max_score))
            return redirect(competition)

        if player_id == '1':
            match.p1_reg_score = p1_score + "-" + p2_score
        elif player_id == '2':
            match.p2_reg_score = p1_score + "-" + p2_score

    if match.p1_reg_score and match.p2_reg_score:
        if match.p1_reg_score == match.p2_reg_score:
            if match.p1_reg_score[0] > match.p1_reg_score[2]:
                match.final_score = match.p1_reg_score
                match.winner = match.player1
            elif match.p1_reg_score[0] < match.p1_reg_score[2]:
                match.final_score = match.p1_reg_score
                match.winner = match.player2
            else:
                match.save()
                reporting_error(match)
                return redirect(competition)
            complete_match(competition, match)
        else:
            reporting_error(match)
    match.save()
    return redirect(competition)


def complete_match(competition, match):
    challonge.set_credentials(settings.CHALLONGE_API_USERNAME, settings.CHALLONGE_API_KEY)
    challonge.matches.update(competition.challonge_url, match.matchid, scores_csv=match.final_score,
                             winner_id=match.winner.cid)
    match.state = 'complete'
    match.save()
    update_match_list(competition)
    if not Match.objects.filter(competition=competition, state='open'):
        competition.status = 4
        challonge.tournaments.finalize(competition.challonge_url)
        competition.save()


def reporting_error(match):
    match.state = 'error'
    match.save()


@staff_member_required
@login_required
def submit_score(request, competition_id, match_id):
    competition = get_object_or_404(Competition, pk=competition_id)
    match = get_object_or_404(Match, matchid=match_id, competition=competition)
    if request.method == 'POST':
        final_score = request.POST.get('final_score')
        print final_score
        winner = request.POST.get('winner')
        match.winner = Participant.objects.get(competition=competition, cid=winner)
        match.final_score = final_score
        complete_match(competition, match)
    match.save()
    return redirect(competition)
