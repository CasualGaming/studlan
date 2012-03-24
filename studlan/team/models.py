# -*- coding: utf-8 -*-

from django.contrib.auth.models import User
from django.db import models



class Team(models.Model):
    
    title = models.CharField('title', max_length=50)
    tag = models.CharField('tag', max_length=10, unique=True)
    leader = models.ForeignKey(User, blank=False, related_name="newteamleader")
    members = models.ManyToManyField(User, related_name='new_team_members', through='Member')

    @models.permalink
    def get_absolute_url(self):
        return ('team', (), {'team_tag': self.tag})

    def __unicode__(self):
        return '[%s] %s' % (self.tag, self.title)

    class Meta:
        ordering = ['tag', 'title']

class Member(models.Model):
    team = models.ForeignKey(Team)
    user = models.ForeignKey(User)
    date_joined = models.DateTimeField("date joined", auto_now_add=True)

    def __unicode__(self):
        return self.user.username
        
    class Meta:
        unique_together = ('team', 'user',)
        ordering = ['user']
