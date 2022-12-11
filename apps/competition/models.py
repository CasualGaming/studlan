# -*- coding: utf-8 -*-

from django.contrib.auth.models import User
from django.db import models
from django.db.models import Q
from django.urls import reverse
from django.utils.translation import pgettext_lazy, ugettext, ugettext_lazy as _

from apps.lan.models import LAN
from apps.userprofile.models import AliasType


class Activity(models.Model):
    title = models.CharField(_('title'), max_length=50)
    image_url = models.CharField(_('image URL'), max_length=100, blank=True,
                                 help_text=_('Use a mirrored image of at least a height of 150px.'))
    desc = models.TextField(_('description'), blank=True)

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('activity_details', kwargs={'activity_id': self.id})

    class Meta:
        verbose_name = _('activity')
        verbose_name_plural = _('activities')
        ordering = ['title']


class Competition(models.Model):
    STATUSES = (
        (1, pgettext_lazy('competition status', 'Open')),
        (2, pgettext_lazy('competition status', 'Closed')),
        (3, pgettext_lazy('competition status', 'In progress')),
        (4, pgettext_lazy('competition status', 'Finished')),
    )
    STATUS_LABELS = [
        'success',
        'warning',
        'info',
        'danger',
    ]
    TOURNAMENT_FORMATS = (
        ('single elimination', _('Single elimination')),
        ('double elimination', _('Double elimination')),
    )

    status = models.SmallIntegerField(_('status'), choices=STATUSES)
    activity = models.ForeignKey(Activity, verbose_name=_('activity'), on_delete=models.CASCADE)
    lan = models.ForeignKey(LAN, verbose_name=_('LAN'), on_delete=models.CASCADE)
    challonge_url = models.CharField(_('Challonge URL'), max_length=50, null=True, blank=True,
                                     help_text='Do not set this field if challonge integration is enabled. '
                                               'The challonge url will be generated after starting the competition.')
    team_size = models.IntegerField(_('team size'), default=5, blank=True)
    start_time = models.DateTimeField(_('start time'), null=True, blank=True)
    tournament_format = models.CharField(
        _('tournament format'), max_length=20, null=True, blank=True, choices=TOURNAMENT_FORMATS,
        help_text='Only set this field if the Challonge integration is being used for this competition.')
    max_participants = models.SmallIntegerField(
        _('maximum participants'), default=0, help_text=_('The maximum number of participants allowed for a competition.'
                                                           ' Restricts participants based on competition type. 0 means'
                                                           ' infinite participants are allowed.'))
    use_teams = models.BooleanField(
        _('use teams'), default=False, help_text=_('If checked, participants will be ignored, and will '
                                                    'instead use teams. If left unchecked teams will be ignored, '
                                                    'and participants will be used.'))
    enforce_team_size = models.BooleanField(
        _('enforce teams'), default=False, help_text=_('If checked, teams will require x members (specified in team_size)'
                                                        ' before being able to sign up.'))
    enforce_payment = models.BooleanField(
        _('enforce payment'), default=False, help_text=_('If checked, teams will require x members (specified in team_size)'
                                                          ' with valid tickets before being able to sign up.'))
    require_alias = models.BooleanField(
        _('require alias'), default=False, help_text=_('If checked, players will need to register an alias for the '
                                                        'activity that the competition belongs to.'))
    max_match_points = models.SmallIntegerField(
        _('maximum match points'), default=1, help_text=_('This number represents how many points are needed to win '
                                                           'a match. E.g. 3 in a BO 5 or 16 in BO 30'))


    def get_teams(self):
        if self.use_teams:
            return [getattr(x, 'team') for x in Participant.objects.filter(~Q(team=None), Q(competition=self))]
        else:
            return []

    def get_users(self):
        return [getattr(x, 'user') for x in Participant.objects.filter(~Q(user=None), Q(competition=self))]

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
        return Participant.objects.filter(Q(competition=self) & (Q(user=user) | Q(team__leader=user) | Q(team__member__user=user))).exists()

    def has_alias(self, user):
        return AliasType.objects.filter(activity=self.activity, alias__user=user).exists()

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
        return self.STATUSES[self.status - 1][1]

    def status_label(self):
        return self.STATUS_LABELS[self.status - 1]

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
        verbose_name = _('competition')
        verbose_name_plural = _('competitions')
        ordering = ['status']
        permissions = (
            ('manage', 'Manage compos and matches'),
        )



class Participant(models.Model):
    user = models.ForeignKey(User, verbose_name=_('user'), null=True, on_delete=models.CASCADE)
    team = models.ForeignKey('team.Team', verbose_name=_('team'), null=True, on_delete=models.CASCADE)
    competition = models.ForeignKey(Competition, verbose_name=_('competition'), on_delete=models.CASCADE)
    cid = models.CharField(_('cid'), max_length=50, null=True, blank=True)

    def __unicode__(self):
        if self.user:
            return self.user.username
        else:
            return str(self.team)

    def is_team(self):
        if self.user:
            return False
        else:
            return True

    class Meta:
        verbose_name = _('competition participant')
        verbose_name_plural = _('competition participants')
        unique_together = (
            ('user', 'competition'),
            ('team', 'competition'),
        )
        ordering = ['user', 'team']


class Match(models.Model):
    matchid = models.CharField(_('match ID'), max_length=50)
    player1 = models.ForeignKey(Participant, verbose_name=_('player 1'), related_name='player1', null=True, on_delete=models.CASCADE)
    player2 = models.ForeignKey(Participant, verbose_name=_('player 2'), related_name='player2', null=True, on_delete=models.CASCADE)
    competition = models.ForeignKey(Competition, verbose_name=_('competition'), on_delete=models.CASCADE)
    p1_reg_score = models.CharField(_('p1 reg score'), max_length=50, null=True, blank=True)
    p2_reg_score = models.CharField(_('p2 reg score'), max_length=50, null=True, blank=True)
    final_score = models.CharField(_('final score'), max_length=50, null=True, blank=True)
    state = models.CharField(_('state'), max_length=50)
    winner = models.ForeignKey(Participant, verbose_name=_('winner'), related_name='winner', null=True, blank=True, on_delete=models.CASCADE)

    def get_p1(self):
        if self.player1:
            if self.player1.is_team:
                return self.player1.team
            else:
                return self.player1.user
        else:
            return ugettext('TBA')

    def get_p2(self):
        if self.player2:
            if self.player2.is_team:
                return self.player2.team
            else:
                return self.player2.user
        else:
            return ugettext('TBA')

    def get_compo(self):
        return self.competition.activity.title

    def get_lan(self):
        return self.competition.lan.title

    def is_valid_score_reporter(self, user, player_id):
        if self.player1.team is None and self.player2.team is None:
            if (user == self.player1.user and player_id == '1') or (user == self.player2.user and player_id == '2'):
                return True
        else:
            if (user == self.player1.team.leader and player_id == '1')\
                    or (user == self.player2.team.leader and player_id == '2'):
                return True
            if (user in self.player1.team.members.all() and player_id == '1')\
                    or (user in self.player2.team.members.all() and player_id == '2'):
                return True
        return False

    class Meta:
        verbose_name = _('competition match')
        verbose_name_plural = _('competition matches')
