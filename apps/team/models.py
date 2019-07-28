# -*- coding: utf-8 -*-

from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _lazy

from apps.lan.models import Attendee


class Team(models.Model):
    title = models.CharField(_lazy(u'title'), max_length=50)
    tag = models.CharField(_lazy(u'tag'), max_length=10, unique=True)
    # Warning: Leader is (generally?) not included in members
    leader = models.ForeignKey(User, verbose_name=_lazy(u'leader'), blank=False, related_name='newteamleader')
    members = models.ManyToManyField(User, verbose_name=_lazy(u'members'), related_name='new_team_members', through='Member')

    def get_absolute_url(self):
        return reverse('show_team', kwargs={'team_id': self.id})

    def number_of_team_members(self):
        return Member.objects.filter(team=self).count()

    def number_of_aliases(self, competition):
        aliases = 0
        if competition.has_alias(self.leader):
            aliases += 1
        for member in self.members.all():
            if competition.has_alias(member):
                aliases += 1
        return aliases

    def number_of_attending_members(self, lan):
        attending = 0
        if self.leader in lan.attendees:
            attending += 1
        for member in self.members.all():
            if member in lan.attendees:
                attending += 1
        return attending

    def number_of_paid_members(self, lan):
        paid = 0
        if self.leader in lan.attendees:
            leader_attendee = Attendee.objects.get(lan=lan, user=self.leader)
            if leader_attendee.has_paid or lan.has_ticket(self.leader):
                paid += 1
        for member in self.members.all():
            if member in lan.attendees:
                attendee = Attendee.objects.get(lan=lan, user=member)
                if attendee.has_paid or lan.has_ticket(member):
                    paid += 1
        return paid

    def __unicode__(self):
        return u'[{0}] {1}'.format(self.tag, self.title)

    class Meta:
        verbose_name = _lazy(u'team')
        verbose_name_plural = _lazy(u'teams')
        ordering = ['tag', 'title']


class Member(models.Model):
    team = models.ForeignKey(Team, verbose_name=_lazy(u'team'))
    user = models.ForeignKey(User, verbose_name=_lazy(u'user'))
    date_joined = models.DateTimeField(_lazy(u'date joined'), auto_now_add=True)

    def __unicode__(self):
        return self.user.username

    class Meta:
        verbose_name = _lazy(u'team member')
        verbose_name_plural = _lazy(u'team members')
        unique_together = ('team', 'user')
        ordering = ['user']


class Invitation(models.Model):
    team = models.ForeignKey(Team, verbose_name=_lazy(u'team'))
    invitee = models.ForeignKey(User, verbose_name=_lazy(u'invitee'), related_name='Invitee')
    token = models.CharField(_lazy(u'token'), max_length=32, editable=False)

    class Meta:
        verbose_name = _lazy(u'team invitation')
        verbose_name_plural = _lazy(u'team invitations')
