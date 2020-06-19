# -*- coding: utf-8 -*-

from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from apps.lan.models import Attendee


class Team(models.Model):
    title = models.CharField(_(u'title'), max_length=50)
    tag = models.CharField(_(u'tag'), max_length=10, unique=True)
    # Warning: Leader is (generally?) not included in members
    leader = models.ForeignKey(User, verbose_name=_(u'leader'), blank=False, related_name='newteamleader')
    members = models.ManyToManyField(User, verbose_name=_(u'members'), related_name='new_team_members', through='Member')

    @property
    def full_member_count(self):
        # Team leader not included
        return Member.objects.filter(team=self).count() + 1

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
        verbose_name = _(u'team')
        verbose_name_plural = _(u'teams')
        ordering = ['tag', 'title']
        permissions = (
            ('show_invitations', u'Show users invited to teams'),
        )


class Member(models.Model):
    team = models.ForeignKey(Team, verbose_name=_(u'team'), on_delete=models.CASCADE)
    user = models.ForeignKey(User, verbose_name=_(u'user'), on_delete=models.CASCADE)
    date_joined = models.DateTimeField(_(u'date joined'), auto_now_add=True)

    def __unicode__(self):
        return self.user.username

    class Meta:
        verbose_name = _(u'team member')
        verbose_name_plural = _(u'team members')
        unique_together = ('team', 'user')
        ordering = ['user']


class Invitation(models.Model):
    team = models.ForeignKey(Team, verbose_name=_(u'team'), on_delete=models.CASCADE)
    invitee = models.ForeignKey(User, verbose_name=_(u'invitee'), on_delete=models.CASCADE)
    token = models.CharField(_(u'token'), max_length=32, editable=False)

    class Meta:
        verbose_name = _(u'team invitation')
        verbose_name_plural = _(u'team invitations')
