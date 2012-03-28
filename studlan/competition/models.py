#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.db import models
import datetime

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


class Competition(models.Model):

    STATUS_OPTIONS = ((1, 'Open'), (2, 'Closed'), (3, 'In progress'),
                      (4, 'Finished'))
    statuses = {
        1: ['Registration open', 'success'],
        2: ['Registration closed', 'danger'],
        3: ['Competition in progress', 'warning'],
        4: ['Competition finished', 'info'],
        }
    title = models.CharField('title', max_length=50)
    status = models.SmallIntegerField('status', choices=STATUS_OPTIONS)
    activity = models.ForeignKey(Activity)
    use_teams = models.BooleanField('use teams', default=False,
                                    help_text='If checked, participants'
                                    ' will be ignored, and will '
                                    'instead use teams. If left '
                                    'unchecked teams will be ignored, '
                                    'and participants will be used.')

    desc = models.TextField('description',
                            help_text='Markdown-enabled. You may also '
                            'use regular (x)HTML markup. For '
                            'blockquotes use the following '
                            'markup:<br/><br/>&lt;blockquote&gt;<br/>&n'
                            'bsp;&nbsp;&nbsp;&nbsp;&lt;p&gt;Quote-text&'
                            'lt;/p&gt;<br/>&nbsp;&nbsp;&nbsp;&nbsp;&lt;'
                            'small&gt;Reference&lt;/small&gt;<br/>&lt;/'
                            'blockquote&gt;')

    def __unicode__(self):
        return self.title

    def get_teams(self):
        if self.use_teams:
            return map(lambda x: getattr(x, 'team'), Participant.objects.filter(competition=self))
        else:
            return []

    def get_users(self):
        return map(lambda x: getattr(x, 'user'), Participant.objects.filter(competition=self))

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
        ordering = ['status', 'title']

class Participant(models.Model):
    user = models.ForeignKey(User, null=True)
    team = models.ForeignKey('team.Team', null=True)
    competition = models.ForeignKey(Competition)

    def __unicode__(self):
        if self.user:
            return self.user.get_full_name()
        else:
            return str(self.team)

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
