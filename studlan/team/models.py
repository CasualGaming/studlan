# -*- coding: utf-8 -*-

from django.contrib.auth.models import User
from django.db import models



class Team(models.Model):
    
    title = models.CharField('title', max_length=50)
    tag = models.CharField('tag', max_length=10, unique=True)
    leader = models.ForeignKey(User, blank=False, related_name="newteamleader")
    members = models.ManyToManyField(User, related_name='new_team_members',
            blank=True)

    def __unicode__(self):
        return '[%s]%s' % (self.tag, self.title)

    class Meta:
        ordering = ['tag', 'title']
