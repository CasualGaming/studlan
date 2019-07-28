# -*- coding: utf-8 -*-

from django.contrib.auth.models import User
from django.db import models
from django.db.models import Q
from django.urls import reverse
from django.utils.translation import ugettext as _, ugettext_lazy as _lazy

from translatable.models import TranslatableModel, get_translation_model

from apps.lan.models import LAN
from apps.userprofile.models import Alias, AliasType


class Activity(models.Model):

    title = models.CharField(_lazy(u'title'), max_length=50)
    image_url = models.CharField(_lazy(u'image url'), max_length=100, blank=True,
                                 help_text=_lazy(u'Use a mirrored image of at least a height of 150px.'))
    desc = models.TextField(_lazy(u'description'), blank=True)

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('activity_details', kwargs={'activity_id': self.id})

    class Meta:
        verbose_name = _lazy(u'activity')
        verbose_name_plural = _lazy(u'activities')
        ordering = ['title']


class Competition(TranslatableModel):

    STATUS_OPTIONS = ((1, _lazy(u'Open')), (2, _lazy(u'Closed')), (3, _lazy(u'In progress')),
                      (4, _lazy(u'Finished')))

    TOURNAMENT_FORMATS = (('single elimination', _lazy(u'Single elimination')), ('double elimination', _lazy(u'Double elimination')))

    statuses = {
        1: [_lazy(u'Registration open'), 'success'],
        2: [_lazy(u'Registration closed'), 'danger'],
        3: [_lazy(u'Competition in progress'), 'warning'],
        4: [_lazy(u'Competition finished'), 'info'],
    }

    status = models.SmallIntegerField(_lazy(u'status'), choices=STATUS_OPTIONS)
    activity = models.ForeignKey(Activity, verbose_name=_lazy(u'activity'))
    lan = models.ForeignKey(LAN, verbose_name=_lazy(u'lan'))
    challonge_url = models.CharField(_lazy(u'Challonge URL'), max_length=50, blank=True)
    team_size = models.IntegerField(_lazy(u'team size'), default=5, blank=True)
    start_time = models.DateTimeField(_lazy(u'start time'), blank=True, null=True)

    tournament_format = models.CharField(
        _lazy(u'tournament format'), max_length=20, blank=True, choices=TOURNAMENT_FORMATS)

    max_participants = models.SmallIntegerField(
        _lazy(u'maximum participants'), default=0, help_text=_lazy(u'The maximum number of participants allowed for a competition.'
                                                                   'Restricts participants based on competition type. 0 means'
                                                                   ' infinite participants are allowed.'))

    use_teams = models.BooleanField(
        _lazy(u'use teams'), default=False, help_text=_lazy(u'If checked, participants will be ignored, and will '
                                                            'instead use teams. If left unchecked teams will be ignored, '
                                                            'and participants will be used.'))

    enforce_team_size = models.BooleanField(
        _lazy(u'enforce teams'), default=False, help_text=_lazy(u'If checked, teams will require x members (specified in team_size)'
                                                                ' before being able to sign up.'))

    enforce_payment = models.BooleanField(
        _lazy(u'enforce payment'), default=False, help_text=_lazy(u'If checked, teams will require x members (specified in team_size)'
                                                                  ' with valid tickets before being able to sign up.'))

    require_alias = models.BooleanField(
        _lazy(u'require alias'), default=False, help_text=_lazy(u'If checked, players will need to register an alias for the '
                                                                'Activity that the competition belongs to.'))

    max_match_points = models.SmallIntegerField(
        _lazy(u'maximum match points'), default=1, help_text=_lazy(u'This number represents how many points are needed to win '
                                                                   'a match. E.g. 3 in a BO 5 or 16 in BO 30'))

    def get_teams(self):
        if self.use_teams:
            return map(lambda x: getattr(x, 'team'), Participant.objects.filter(~Q(team=None), Q(competition=self)))
        else:
            return []

    def get_users(self):
        return map(lambda x: getattr(x, 'user'), Participant.objects.filter(~Q(user=None), Q(competition=self)))

    def get_participants(self):
        participants = Participant.objects.filter(competition=self)
        teams = []
        users = []
        for participant in participants:
            if participant.is_team():
                teams.append(participant.team)
            else:
                users.append(participant.user)

        return teams, users

    def has_participant(self, user):
        if user in self.get_users():
            return True
        for team in self.get_teams():
            if user == team.leader or user in team.members.all():
                return True

    def has_alias(self, user):
        if AliasType.objects.filter(activity=self.activity).exists():
            alias_types = AliasType.objects.get(activity=self.activity)
            for alias_type in alias_types:
                if Alias.objects.filter(user=user, alias_type=alias_type).exists():
                    return True
        return False

    def participant_spots_free(self):
        teams, users = self.get_participants()
        if self.max_participants > 0:
            if self.use_teams:
                return self.max_participants - len(teams)
            else:
                return self.max_participants - len(users)
        else:
            return -1

    def status_text(self):
        return self.STATUS_OPTIONS[self.status - 1][1]

    def status_text_verbose(self):
        return self.statuses[self.status][0]

    def status_label(self):
        return self.statuses[self.status][1]

    def get_absolute_url(self):
        return reverse('competition_details', kwargs={'competition_id': self.id})

    @staticmethod
    def get_all_for_user(user, ignore_finished=False):
        user_participations = Participant.objects.filter(user=user).select_related('competition').order_by('competition__status')
        if ignore_finished:
            user_participations = user_participations.filter(~Q(competition__status=4))

        team_participations = Participant.objects.filter(Q(team__members=user) | Q(team__leader=user)).order_by('competition__status')
        if ignore_finished:
            team_participations = team_participations.filter(~Q(competition__status=4))

        competitions = [p.competition for p in user_participations] + [p.competition for p in team_participations]
        return competitions

    class Meta:
        verbose_name = _lazy(u'competition')
        verbose_name_plural = _lazy(u'competitions')
        ordering = ['status']
        permissions = (
            ('manage', 'Manage compos and matches'),
        )


class CompetitionTranslation(get_translation_model(Competition, 'competition')):
    translated_title = models.CharField(_lazy(u'title'), max_length=50)
    translated_description = models.TextField(_lazy(u'description'))

    def __unicode__(self):
        return self.translated_title

    class Meta:
        verbose_name = _lazy(u'competition translation')
        verbose_name_plural = _lazy(u'competition translations')


class Participant(models.Model):
    user = models.ForeignKey(User, verbose_name=_lazy(u'user'), null=True)
    team = models.ForeignKey('team.Team', verbose_name=_lazy(u'team'), null=True)
    competition = models.ForeignKey(Competition, verbose_name=_lazy(u'competition'))
    # Nullable (x3)
    cid = models.CharField(_lazy(u'cid'), max_length=50, null=True, blank=True)

    def __unicode__(self):
        if self.user:
            return self.user.username
        else:
            return unicode(self.team)

    def is_team(self):
        if self.user:
            return False
        else:
            return True

    class Meta:
        verbose_name = _lazy(u'competition participant')
        verbose_name_plural = _lazy(u'competition participants')
        unique_together = (
            ('user', 'competition'),
            ('team', 'competition'),
        )
        ordering = ['user', 'team']


class Match(models.Model):
    matchid = models.CharField(_lazy(u'match ID'), max_length=50)
    player1 = models.ForeignKey(Participant, verbose_name=_lazy(u'player 1'), related_name='player1', null=True)
    player2 = models.ForeignKey(Participant, verbose_name=_lazy(u'player 2'), related_name='player2', null=True)
    competition = models.ForeignKey(Competition, verbose_name=_lazy(u'competition'))
    # Nullable (x3)
    p1_reg_score = models.CharField(_lazy(u'p1 reg score'), max_length=50, null=True, blank=True)
    p2_reg_score = models.CharField(_lazy(u'p2 reg score'), max_length=50, null=True, blank=True)
    final_score = models.CharField(_lazy(u'final score'), max_length=50, null=True, blank=True)
    state = models.CharField(_lazy(u'state'), max_length=50)
    winner = models.ForeignKey(Participant, verbose_name=_lazy(u'winner'), related_name='winner', null=True)

    def get_p1(self):
        if self.player1:
            if self.player1.is_team:
                return self.player1.team
            else:
                return self.player1.user
        else:
            return _(u'TBA')

    def get_p2(self):
        if self.player2:
            if self.player2.is_team:
                return self.player2.team
            else:
                return self.player2.user
        else:
            return _(u'TBA')

    def get_compo(self):
        return self.competition.activity.title

    def get_lan(self):
        return self.competition.lan.title

    def is_valid_score_reporter(self, user, player_id):
        if self.player1.team is None and self.player2.team is None:
            if (user == self.player1.user and player_id == '1') or (user == self.player2.user and player_id == '2'):
                return True
        else:
            if user == (self.player1.team.leader and player_id == '1')\
                    or user == (self.player2.team.leader and player_id == '2'):
                return True
            if user in (self.player1.team.members.all() and player_id == '1')\
                    or (user in self.player2.members.all() and player_id == '2'):
                return True
        return False

    class Meta:
        verbose_name = _lazy(u'competition match')
        verbose_name_plural = _lazy(u'competition matches')
