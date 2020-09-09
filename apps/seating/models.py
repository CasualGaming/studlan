# -*- coding: utf-8 -*-

import datetime

from django.contrib.auth.models import User
from django.db import models
from django.db.models import Q
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from apps.lan.models import LAN, TicketType


class Layout(models.Model):
    title = models.CharField(_(u'title'), max_length=50)
    description = models.CharField(_(u'description'), max_length=250)
    number_of_seats = models.IntegerField(_(u'number of seats'))
    template = models.TextField(_(u'SVG layout for seating'), null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.pk:
            super(Layout, self).save(*args, **kwargs)
        else:
            super(Layout, self).save(*args, **kwargs)
            dependant_seatings = Seating.objects.filter(layout=self)
            for seating in dependant_seatings:
                seating.number_of_seats = self.number_of_seats
                seating.save()

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = _(u'seating layout')
        verbose_name_plural = _(u'seating layouts')


class Seating(models.Model):
    lan = models.ForeignKey(LAN, verbose_name=_(u'LAN'))
    title = models.CharField(_(u'title'), max_length=50)
    desc = models.CharField(_(u'description'), max_length=250)
    number_of_seats = models.IntegerField(_(u'number of seats'), default=0, help_text=_(u'This field is automatically updated '
                                          'to match the chosen layout. Change the chosen layout to alter this field.'))
    closing_date = models.DateTimeField(_(u'closing date'))
    layout = models.ForeignKey(Layout, verbose_name=_(u'layout'))
    ticket_types = models.ManyToManyField(TicketType, verbose_name=_(u'ticket types'), blank=True, related_name='ticket_types')

    def save(self, *args, **kwargs):
        if not self.pk:
            self.number_of_seats = self.layout.number_of_seats
            super(Seating, self).save(*args, **kwargs)
            self.populate_seats()
        else:
            self.number_of_seats = self.layout.number_of_seats
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
        return u'{0} / {1}'.format(self.lan, self.title)

    def get_absolute_url(self):
        return reverse('seating_details', kwargs={'lan_id': self.lan.id, 'seating_id': self.id})

    def populate_seats(self):
        for k in range(0, self.number_of_seats):
            seat = Seat(seating=self, placement=k + 1)
            seat.save()

    class Meta:
        verbose_name = _(u'seating')
        verbose_name_plural = _(u'seatings')
        permissions = (
            ('export_seating', u'Can export seating to downloadable file'),
        )


class Seat(models.Model):
    user = models.ForeignKey(User, verbose_name=_(u'user'), null=True, blank=True)
    seating = models.ForeignKey(Seating, verbose_name=_(u'seating'))
    placement = models.IntegerField(_(u'placement ID'), help_text=_(u'A unique ID within the seating.'))

    def __unicode__(self):
        return u'{0} / {1} / {2}'.format(self.seating.lan, self.seating.title, self.placement)

    def get_absolute_url(self):
        return reverse('seating_details', kwargs={'lan_id': self.seating.lan.id, 'seating_id': self.seating.id, 'seat_id': self.placement})

    class Meta:
        verbose_name = _(u'seat')
        verbose_name_plural = _(u'seats')
        ordering = ['seating', 'placement']
