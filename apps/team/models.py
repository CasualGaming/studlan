# -*- coding: utf-8 -*-

from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse

from apps.lan.models import Attendee


class Team(models.Model):
    title = models.CharField('title', max_length=50)
    tag = models.CharField('tag', max_length=10, unique=True)
    # Warning: Leader is (generally?) not included in members
    leader = models.ForeignKey(User, blank=False, related_name='newteamleader')
    members = models.ManyToManyField(User, related_name='new_team_members', through='Member')

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
        ordering = ['tag', 'title']


class Member(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_joined = models.DateTimeField('date joined', auto_now_add=True)

    def __unicode__(self):
        return self.user.username

    class Meta:
        unique_together = ('team', 'user')
        ordering = ['user']


class Invitation(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    invitee = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField('token', max_length=32, editable=False)
