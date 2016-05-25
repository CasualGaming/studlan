# -*- coding: utf-8 -*-

import datetime

from django.contrib.auth.models import User
from django.db import models
from django.db.models import Q

from apps.lan.models import LAN, TicketType


class Layout(models.Model):
    title = models.CharField('title', max_length=50)
    description = models.CharField('description', max_length=250)
    number_of_seats = models.IntegerField('number of seats')
    template = models.TextField('SVG layout for seating', null=True, blank=True)

    def __unicode__(self):
        return self.title


class Seating(models.Model):
    lan = models.ForeignKey(LAN)
    title = models.CharField('title', max_length=50)
    desc = models.CharField('description', max_length=250)
    number_of_seats = models.IntegerField('number of seats')
    closing_date = models.DateTimeField("closing date")
    layout = models.ForeignKey(Layout)
    ticket_types = models.ManyToManyField(TicketType, null=True, blank=True, related_name='ticket_types')

    def save(self, *args, **kwargs):
        if not self.pk:
            super(Seating, self).save(*args, **kwargs)
            self.populate_seats()
        else:
            super(Seating, self).save(*args, **kwargs)

    def get_user_registered(self):
        return map(lambda x: getattr(x, 'user'), Seat.objects.filter(~Q(user=None), Q(seating=self)))

    def get_total_seats(self):
        return Seat.objects.filter(Q(seating=self)).order_by('placement')

    def get_number_of_seats(self):
        return Seat.objects.filter(Q(seating=self)).count()

    def is_open(self):
        return datetime.datetime.now() < self.closing_date

    def get_free_seats(self):
        return Seat.objects.filter(Q(user=None), Q(seating=self)).count()

    def __unicode__(self):
        return self.title

    @models.permalink
    def get_absolute_url(self):
        return ('seating_details', (), {'lan_id': self.lan.id, 'seating_id': self.id})

    def populate_seats(self):
        for k in range(0, self.number_of_seats):
            seat = Seat(seating=self, placement=k+1)
            seat.save()


class Seat(models.Model):
    user = models.ForeignKey(User, null=True, blank=True)
    seating = models.ForeignKey(Seating)
    placement = models.IntegerField("placement id")

    def __unicode__(self):
        return str(self.id)