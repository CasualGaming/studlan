#!/usr/bin/python
# -*- coding: utf-8 -*-

import datetime
from translatable.models import TranslatableModel, get_translation_model

from django.contrib.auth.models import User
from django.db import models
from django.db.models import Q
from django.db.models.signals import post_save
from django.utils import translation
from django.utils.translation import ugettext as _

from apps.lan.models import LAN
from apps.userprofile.models import Alias, AliasType


class Activity(models.Model):

    title = models.CharField('title', max_length=50)
    image_url = models.CharField('Image url', max_length=100, blank=True,
                                 help_text='Use a mirrored image of at least a height of 150px.')
    desc = models.TextField('description')

    def __unicode__(self):
        return self.title

    @models.permalink
    def get_absolute_url(self):
        return ('activity_details', (), {'activity_id': self.id})

    class Meta:
        ordering = ['title']
        verbose_name = 'activity'
        verbose_name_plural = 'activities'


class Competition(TranslatableModel):

    STATUS_OPTIONS = ((1, _(u'Open')), (2, _(u'Closed')), (3, _(u'In progress')),
                      (4, _(u'Finished')))
    statuses = {
        1: ['Registration open', 'success'],
        2: ['Registration closed', 'danger'],
        3: ['Competition in progress', 'warning'],
        4: ['Competition finished', 'info'],
    }

    status = models.SmallIntegerField('status', choices=STATUS_OPTIONS)
    activity = models.ForeignKey(Activity)
    lan = models.ForeignKey(LAN)
    challonge_url = models.CharField('Challonge url', max_length=50, blank=True, null=True)
    use_teams = models.BooleanField('use teams', default=False,
                                    help_text='If checked, participants will be ignored, and will '
                                    'instead use teams. If left unchecked teams will be ignored, '
                                    'and participants will be used.')
    team_size = models.IntegerField(default=5, blank=True)
    enforce_team_size = models.BooleanField('enforce teams', default=False,
                                            help_text='If checked, teams will require x members (specified in team_size) before being able '
                                            'to sign up.')
    enforce_payment = models.BooleanField('enforce payment', default=False,
                                            help_text='If checked, teams will require x members (specified in team_size) with valid tickets before'
                                          ' being able to sign up.')
    require_alias = models.BooleanField('require alias', default=False, help_text="If checked, players will need to register"
                                        "an alias for the Activity that the competition belongs to.")
    start_time = models.DateTimeField(blank=True, null=True)


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
            alias_type = AliasType.objects.get(activity=self.activity)
            if Alias.objects.filter(user=user, alias_type=alias_type).exists():
                return True
            else:
                return False
        else:
            return False

    def status_text(self):
        return self.STATUS_OPTIONS[self.status - 1][1]

    def status_text_verbose(self):
        return self.statuses[self.status][0]

    def status_label(self):
        return self.statuses[self.status][1]
    
    @models.permalink
    def get_absolute_url(self):
        return ('competition_details', (), {'competition_id': self.id})

    class Meta:
        ordering = ['status',]


class CompetitionTranslation(get_translation_model(Competition, "competition")):
    translated_title = models.CharField('title', max_length=50)
    translated_description = models.TextField('description',
        help_text='Markdown-enabled. You may also use regular (x)HTML markup. For '
        'blockquotes use the following markup:<br/><br/>&lt;blockquote&gt;<br/>&n'
        'bsp;&nbsp;&nbsp;&nbsp;&lt;p&gt;Quote-text& lt;/p&gt;<br/>&nbsp;&nbsp;&nbsp;&nbsp;&lt;'
        'small&gt;Reference&lt;/small&gt;<br/>&lt;/blockquote&gt;')
    
    def __unicode__(self):
        return self.translated_title


class Participant(models.Model):
    user = models.ForeignKey(User, null=True)
    team = models.ForeignKey('team.Team', null=True)
    competition = models.ForeignKey(Competition)
    cid = models.CharField('cid', max_length=50, null=True)

    def __unicode__(self):
        if self.user:
            return self.user.get_full_name()
        else:
            return unicode(self.team)

    def is_team(self):
        if self.user:
            return False
        else:
            return True

    class Meta:
        unique_together = (
            ('user', 'competition',),
            ('team', 'competition',),
        )
        ordering = ['user', 'team']


class Match(models.Model):
    matchid = models.CharField('matchid', max_length=50)
    player1 = models.ForeignKey(Participant, related_name='player1', null=True)
    player2 = models.ForeignKey(Participant, related_name='player2', null=True)
    competition = models.ForeignKey(Competition)
    p1_reg_score = models.CharField('p1_reg_score', max_length=50, null=True)
    p2_reg_score = models.CharField('p2_reg_score', max_length=50, null=True)
    final_score = models.CharField('final_score', max_length=50, null=True)
    state = models.CharField('state', max_length=50)
    winner = models.ForeignKey(Participant, related_name='winner', null=True)

    def get_p1(self):
        if self.player1:
            if self.player1.is_team:
                return self.player1.team
            else:
                return self.player1.user
        else:
            return "TBA"

    def get_p2(self):
        if self.player2:
            if self.player2.is_team:
                return self.player2.team
            else:
                return self.player2.user
        else:
            return "TBA"

    def get_compo(self):
        return self.competition.activity.title

    def get_lan(self):
        return self.competition.lan.title
