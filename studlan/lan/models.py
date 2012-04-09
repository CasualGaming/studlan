# -*- coding: utf-8 -*-

from datetime import datetime

from django.contrib.auth.models import User
from django.db import models

class LAN(models.Model):
    title = models.CharField("title", max_length=100)
    start_date = models.DateTimeField("start date")
    end_date = models.DateTimeField("end date")
    location = models.CharField("location", max_length=100)
    description = models.TextField("description")

    def status(self):
        now = datetime.now()
        if now < start_date:
            return 'upcoming'
        else:
            if now < end_date:
                return 'in progress'
            else:
                return 'ended'

    @models.permalink
    def get_absolute_url(self):
        return ('lan_details', (), {'lan_id': self.id})

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ['-start_date']

class Attendee(models.Model):
    user = models.ForeignKey(User)
    lan = models.ForeignKey(LAN)
    has_paid = models.BooleanField("has paid")

    def __unicode__(self):
        return user.get_full_name() + " - " + lan.title

    class Meta:
        ordering = ['user', 'lan',]
