#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.db import models


class Activity(models.Model):

    title = models.CharField('title', max_length=50)
    image_url = models.CharField('Image url', max_length=100,
                                 blank=True,
                                 help_text='Use a mirrored image of at '
                                 'least a height of 150px.')
    desc = models.TextField('description')

    def __unicode__(self):
        return self.title

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
    participants = models.ManyToManyField(User, blank=True)
    teams = models.ManyToManyField('Team', blank=True)
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
            return self.teams.all()
        else:
            return None

    def status_text(self):
        return self.STATUS_OPTIONS[self.status - 1][1]

    def status_text_verbose(self):
        return self.statuses[self.status][0]

    def status_label(self):
        return self.statuses[self.status][1]

    class Meta:

        ordering = ['status', 'title']


class Team(models.Model):

    title = models.CharField('title', max_length=50)
    tag = models.CharField('tag', max_length=10, unique=True)
    size = models.CharField('size', max_length=2)
    leader = models.ForeignKey(User, blank=False)
    members = models.ManyToManyField(User, related_name='team_members',
            blank=True)

    def __unicode__(self):
        return '[%s]%s' % (self.tag, self.title)

    class Meta:

        ordering = ['tag', 'title']


class UserProfile(models.Model):

    user = models.OneToOneField(User)
    nick = models.CharField('nick', max_length=20,
                            help_text='Specify a nick name (display '
                            'name).')

    def __unicode__(self):
        return self.user.username


def create_user_profile(
    sender,
    instance,
    created,
    **kwargs
    ):

    if created:
        UserProfile.objects.create(user=instance)


post_save.connect(create_user_profile, sender=User,
                  dispatch_uid='users-profilecreation-signal')
