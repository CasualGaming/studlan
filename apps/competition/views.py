# -*- coding: utf-8 -*-

import re
import time
from datetime import datetime

import challonge

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import translation
from django.utils.translation import ugettext as _
from django.views.decorators.http import require_POST, require_safe

from apps.competition.models import Activity, Competition, Match, Participant
from apps.lan.models import Attendee, LAN
from apps.lottery.models import Lottery
from apps.poll.models import Poll
from apps.team.models import Team


@require_safe
def main(request):
    lans = LAN.objects.filter(end_date__gte=datetime.now())
    if lans.count() == 1:
        next_lan = lans[0]
        return redirect('competitions_lan_compos', lan_id=next_lan.id)
    else:
        return redirect('competitions_lan_list')


@require_safe
def lan_list(request):
    context = {}
    context['upcoming_lans'] = LAN.objects.filter(end_date__gte=datetime.now()).order_by('start_date')
    context['previous_lans'] = LAN.objects.filter(end_date__lt=datetime.now()).order_by('-start_date')

    return render(request, 'competition/competition_lan_list.html', context)


@require_safe
def lan_compos(request, lan_id):
    lan = get_object_or_404(LAN, pk=lan_id)

    competitions = Competition.objects.filter(lan=lan).order_by('status', 'start_time')

    context = {}
    context['lan'] = lan
    context['activities'] = Activity.objects.all()
    context['competitions'] = competitions
    context['active'] = 'all'
    context['polls'] = Poll.objects.filter(lan=lan)
    context['lotteries'] = Lottery.objects.filter(lan=lan)

    breadcrumbs = (
        (lan, lan.get_absolute_url()),
        (_(u'Competitions'), ''),
    )
    context['breadcrumbs'] = breadcrumbs

    return render(request, 'competition/competitions.html', context)


@require_safe
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

        return render(request, 'competition/competitions.html', context)


@require_safe
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
        (lan, lan.get_absolute_url()),
        (_(u'Competitions'), ''),
    )
    context['breadcrumbs'] = breadcrumbs

    return render(request, 'competition/competitions.html', context)


def shorten_descriptions(competitions, length):
    for c in competitions:
        if len(c.get_translation().translated_description) > length:
            c.get_translation().translated_description = c.get_translation().translated_description[:length - 3] + u'...'
    return competitions


@require_safe
def competition_details(request, competition_id):
    context = {}
    competition = get_object_or_404(Competition, pk=competition_id)
    lan = competition.lan

    # Get challonge settings
    try:
        use_challonge = settings.CHALLONGE_INTEGRATION_ENABLED
        if use_challonge:
            challonge.set_credentials(settings.CHALLONGE_API_USERNAME, settings.CHALLONGE_API_KEY)
    except AttributeError:
        use_challonge = False
    context['use_challonge'] = use_challonge

    breadcrumbs = (
        (lan, lan.get_absolute_url()),
        (_(u'Competitions'), reverse('competitions_lan_compos', kwargs={'lan_id': lan.id})),
        (unicode(competition), ''),
    )
    context['breadcrumbs'] = breadcrumbs

    # Get participants for competition
    teams, users = competition.get_participants()
    context['teams'] = teams
    context['users'] = users

    if request.user.is_authenticated() and competition.has_participant(request.user):
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

        if use_challonge and p:
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
                    messages.warning(request, _(u'You have no current match, please check the brackets for more information.'))

    if request.user.is_authenticated():
        owned_teams = Team.objects.filter(leader=request.user)
        context['owned_teams'] = owned_teams
        context['participating_owned_teams'] = owned_teams.filter(participant__competition=competition)

    context['competition'] = competition

    # Add open or errored matches to context
    if competition.status > 1 and competition.challonge_url and use_challonge:
        context['open_matches'] = Match.objects.filter(
            Q(competition=competition, state='open') | Q(competition=competition, state='error'))
    return render(request, 'competition/competition.html', context)


def update_match_list(request, competition):
    if settings.CHALLONGE_INTEGRATION_ENABLED and settings.CHALLONGE_API_USERNAME != '' and \
            settings.CHALLONGE_API_KEY != '':
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


@require_POST
@login_required
def join(request, competition_id):
    competition = get_object_or_404(Competition, pk=competition_id)
    lan = competition.lan
    user = request.user
    teams, users = competition.get_participants()
    team_id = request.POST.get('team')

    # Checks if the user is already in the competition with a team, solo queue should be
    # overridden by team signup, but not other way around
    participating_user_teams = Team.objects.filter(Q(participant__competition=competition) & (Q(leader=user) | Q(member__user=user)))
    if participating_user_teams.exists():
        messages.error(request, _(u'You are already in this competition with {team}.').format(team=participating_user_teams[0]))
        return redirect(competition)

    # Team sign-up
    if team_id:
        team = get_object_or_404(Team, pk=team_id)

        # Check if team size restrictions are in place
        if competition.enforce_team_size and team.number_of_team_members() + 1 < competition.team_size:
            messages.error(request, _(u'{team} does not have enough members ({current}/{required}).')
                           .format(team=team, current=(team.number_of_team_members() + 1), required=competition.team_size))
            return redirect(competition)

        # Check if payment restrictions are in place
        if competition.enforce_payment:
            if team.number_of_attending_members(competition.lan) < team.number_of_team_members() + 1:
                messages.error(request, _(u'{team} has at least one member that is not signed up for {lan}.').format(team=team, lan=competition.lan))
                return redirect(competition)
            elif team.number_of_paid_members(competition.lan) < competition.team_size:
                messages.error(request, _(u'{team} does not have enough members that have paid ({current}/{required}).')
                               .format(team=team, current=team.number_of_paid_members(competition.lan), required=competition.team_size))
                return redirect(competition)

        # Check if alias restrictions are in place
        if competition.require_alias and team.number_of_aliases(competition) < team.number_of_team_members() + 1:
            if team.number_of_team_members() + 1 - team.number_of_aliases(competition) < 4:
                messages.error(request, _(u'Several members of {team} are missing an alias for {competition}.').format(team=team, competition=competition))
                for member in team.members.all():
                    if not competition.has_alias(member):
                        messages.error(request, _(u'{member} is missing an alias for {competition}.').format(member=member, competition=competition))
                if not competition.has_alias(team.leader):
                    messages.error(request, _(u'{leader} is missing an alias for {competition}.').format(leader=team.leader, competition=competition))
            else:
                messages.error(request, _(u'Several members of {team} are missing an alias for {competition}.').format(team=team, competition=competition))
            return redirect(competition)

        # Go through all members of the team and delete their individual participation entries
        Participant.objects.filter(Q(competition=competition) & (Q(user__newteamleader=team) | Q(user__new_team_members=team))).delete()

        # Add the team
        participant = Participant(team=team, competition=competition)
        participant.save()
        messages.success(request, _(u'You have been signed up for {competition} with team {team}.').format(competition=competition, team=team))

        return redirect(competition)

    # Solo sign-up
    else:
        # Check if already signed up as solo (only for solo sign-up)
        if competition.has_participant(user):
            messages.error(request, _(u'You are already in this competition.'))
            return redirect(competition)

        # Enforce payment
        if competition.enforce_payment:
            attendance = Attendee.objects.filter(lan=lan, user=user)
            if not attendance:
                messages.error(request, _(u'You are not signed up for the LAN.'))
                return redirect(competition)
            has_paid = attendance[0].has_paid or competition.lan.has_ticket(user)
            if not has_paid:
                messages.error(request, _(u'You have not paid for the LAN.'))
                return redirect(competition)

        # Enforce alias
        if competition.require_alias and not competition.has_alias(user):
            messages.error(request, _(u'You do not have the required alias.'))
            return redirect(competition)

        participant = Participant(user=user, competition=competition)
        participant.save()
        messages.success(request, _(u'You have been signed up for {competition}.').format(competition=competition))

        return redirect(competition)


@require_POST
@login_required
def leave(request, competition_id):
    competition = get_object_or_404(Competition, pk=competition_id)

    # If not participating, do nothing
    if not competition.has_participant(request.user):
        messages.error(request, _(u'You are not participating in this competition.'))
        return redirect(competition)

    if request.user in competition.get_users():
        participant = Participant.objects.get(user=request.user, competition=competition)
        participant.delete()
        messages.success(request, _(u'You are no longer participating in {competition}.').format(competition=competition))
    else:
        was_leader = False
        for team in competition.get_teams():
            if request.user == team.leader:
                was_leader = True
                participant = Participant.objects.get(team=team, competition=competition)
                participant.delete()
                messages.success(request, _(u'You have removed {team} from {competition}.').format(team=team, competition=competition))
        if not was_leader:
            messages.error(request, _(u'You cannot remove {team} from {competition}, you are not the team leader.').format(team=team, competition=competition))

    return redirect(competition)


@require_POST
@login_required
def forfeit(request, competition_id):
    competition = get_object_or_404(Competition, pk=competition_id)
    messages.error(request, _(u'Forfeit not yet implemented!'))
    return redirect(competition)


def translate_competitions(competitions):
    translated_competitions = []
    for competition in competitions:
        translated_competitions.append(competition.get_translation(language=translation.get_language()))
    return translated_competitions


@require_safe
def schedule(request):
    lans = LAN.objects.filter(end_date__gt=datetime.now()).order_by('-start_date')

    if lans.count() == 1:
        next_lan = lans[0]
        return redirect('schedule_details', lan_id=next_lan.id)
    else:
        return redirect('schedule_lan_list')


@require_safe
def schedule_lan_list(request):
    context = {}
    context['upcoming_lans'] = LAN.objects.filter(end_date__gte=datetime.now()).order_by('start_date')
    context['previous_lans'] = LAN.objects.filter(end_date__lt=datetime.now()).order_by('-start_date')

    return render(request, 'competition/schedule_lan_list.html', context)


@require_safe
def schedule_details(request, lan_id):
    lan = get_object_or_404(LAN, pk=lan_id)

    context = {}
    context['lan'] = lan
    context['start_date'] = lan.start_date.strftime('%Y%m%d')
    context['end_date'] = lan.end_date.strftime('%Y%m%d')
    if settings.GOOGLE_CAL_SRC != '':
        context['cal_src'] = settings.GOOGLE_CAL_SRC
    else:
        context['cal_src'] = None
    context['breadcrumbs'] = (
        (lan, lan.get_absolute_url()),
        (_(u'Schedule'), ''),
    )

    return render(request, 'competition/schedule.html', context)


@require_POST
@permission_required('competition.manage')
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
                messages.error(request, _(u'Too few participants'))
                return redirect(competition)

            if competition.tournament_format is None:
                messages.error(request, _(u'Set competition tournament format before using this feature.'))
                return redirect(competition)

            if settings.CHALLONGE_INTEGRATION_ENABLED and settings.CHALLONGE_API_USERNAME != '' and \
                    settings.CHALLONGE_API_KEY != '':
                challonge.set_credentials(settings.CHALLONGE_API_USERNAME, settings.CHALLONGE_API_KEY)
                url = unicode(competition.lan) + unicode(competition.activity) + unicode(int(time.time()))
                url = re.sub('[^0-9a-zA-Z]+', '', url)
                challonge.tournaments.create(competition.activity.title, url,
                                             tournament_type=competition.tournament_format)
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
                competition.challonge_url = url
                update_match_list(request, competition)

            competition.status = 3
            competition.save()
            messages.success(request, _(u'Tournament has started.'))
        except Exception:  # noqa: B902: Blind Exception
            messages.error(request, _(u'Something went wrong.'))

    return redirect(competition)


@require_POST
@login_required
def register_score(request, competition_id, match_id, player_id):
    competition = get_object_or_404(Competition, pk=competition_id)
    try:
        match = get_object_or_404(Match, id=match_id, competition=competition)
    except ObjectDoesNotExist:
        messages.error(request, _(u'Match does not exsist.'))
    else:
        if request.method == 'POST':
            if not match.is_valid_score_reporter(request.user, player_id):
                messages.error(request, _(u'You are not authorized to report score for this match.'))
                return redirect(competition)

            max_score = competition.max_match_points
            p1_score = request.POST.get('player1score')
            p2_score = request.POST.get('player2score')

            if int(p1_score) > max_score or int(p1_score) < 0 or int(p2_score) > max_score or int(p2_score) < 0:
                messages.error(request, _(u'Invalid score. Score must be between 0 and {max} (exclusive).').format(max=max_score))
                return redirect(competition)

            if player_id == '1':
                match.p1_reg_score = p1_score + '-' + p2_score
            elif player_id == '2':
                match.p2_reg_score = p1_score + '-' + p2_score

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
                complete_match(request, competition, match)
            else:
                reporting_error(match)
        match.save()
        return redirect(competition)


@require_POST
def complete_match(request, competition, match):
    if settings.CHALLONGE_INTEGRATION_ENABLED and settings.CHALLONGE_API_USERNAME != '' and settings.CHALLONGE_API_KEY != '':
        challonge.set_credentials(settings.CHALLONGE_API_USERNAME, settings.CHALLONGE_API_KEY)
        challonge.matches.update(competition.challonge_url, match.matchid, scores_csv=match.final_score,
                                 winner_id=match.winner.cid)
        match.state = 'complete'
        match.save()
        update_match_list(request, competition)
        if not Match.objects.filter(competition=competition, state='open'):
            competition.status = 4
            challonge.tournaments.finalize(competition.challonge_url)
            competition.save()


def reporting_error(match):
    match.state = 'error'
    match.save()


@require_POST
@permission_required('competition.manage')
def submit_score(request, competition_id, match_id):
    competition = get_object_or_404(Competition, pk=competition_id)
    try:
        match = get_object_or_404(Match, matchid=match_id, competition=competition)
    except (ObjectDoesNotExist):
        messages.error(request, _(u'No match to submit score to.'))
    else:
        if request.method == 'POST':
            final_score = request.POST.get('final_score')
            winner = request.POST.get('winner')
            match.winner = Participant.objects.get(competition=competition, cid=winner)
            match.final_score = final_score
            complete_match(request, competition, match)
        match.save()
    return redirect(competition)
