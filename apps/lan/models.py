# -*- coding: utf-8 -*-

from datetime import datetime

from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _lazy, ugettext_noop as _noop

from translatable.models import TranslatableModel, get_translation_model


class LAN(TranslatableModel):
    title = models.CharField(_lazy(u'title'), max_length=100)
    start_date = models.DateTimeField(_lazy(u'start date'))
    end_date = models.DateTimeField(_lazy(u'end date'))
    location = models.CharField(_lazy(u'location'), max_length=100)
    map_link = models.CharField(_lazy(u'map link'), max_length=300, help_text=_lazy(u'URL for an embedded map'), blank=True)
    video_link = models.CharField(_lazy(u'video link'), max_length=300, help_text=_lazy(u'URL for an embedded video'), blank=True)

    @property
    def attendees(self):
        return map(lambda x: getattr(x, 'user'), Attendee.objects.filter(lan=self))

    @property
    def paid_attendees(self):
        return map(lambda x: getattr(x, 'user'), Attendee.objects.filter(lan=self, has_paid=True))

    def status(self):
        now = datetime.now()
        if now < self.start_date:
            return _noop(u'upcoming')
        else:
            if now < self.end_date:
                return _noop(u'in progress')
            else:
                return _noop(u'ended')

    def tickets(self):
        ticket_types = TicketType.objects.filter(lan=self)

        return Ticket.objects.filter(ticket_type__in=ticket_types)

    def has_ticket(self, user):
        ticket_types = TicketType.objects.filter(lan=self)

        tickets = Ticket.objects.filter(ticket_type__in=ticket_types, user=user)
        if tickets:
            return tickets[0]
        else:
            return None

    def get_absolute_url(self):
        return reverse('lan_details', kwargs={'lan_id': self.id})

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = _lazy(u'LAN')
        verbose_name_plural = _lazy(u'LANs')
        ordering = ['start_date']
        permissions = (
            ('export_paying_participants', u'Can export list of paying participants to downloadable file'),
            ('register_arrivals', u'Can register arrivals'),
            ('register_new_user', u'Can directly register a new user'),
        )


class LANTranslation(get_translation_model(LAN, 'LAN')):
    description = models.TextField(_lazy(u'description'))

    class Meta:
        verbose_name = _lazy(u'LAN translation')
        verbose_name_plural = _lazy(u'LAN translations')


class Attendee(models.Model):
    user = models.ForeignKey(User, verbose_name=_lazy(u'user'))
    lan = models.ForeignKey(LAN, verbose_name=_lazy(u'lan'))
    has_paid = models.BooleanField(_lazy(u'has paid'), default=False)
    arrived = models.BooleanField(_lazy(u'has arrived'), default=False)

    def __unicode__(self):
        return self.user.username + u' – ' + self.lan.title

    def has_paid_or_has_ticket(self):
        return self.has_paid or self.lan.has_ticket(self.user)

    class Meta:
        verbose_name = _lazy(u'LAN attendee')
        verbose_name_plural = _lazy(u'LAN attendees')
        ordering = ['-user', 'lan']
        unique_together = ('user', 'lan')
        index_together = ['user', 'lan']


class TicketType(TranslatableModel):
    lan = models.ForeignKey(LAN, verbose_name=_lazy(u'lan'))

    price = models.IntegerField(_lazy(u'price'), default=50)
    priority = models.IntegerField(_lazy(u'prioity'), default=0, help_text=_lazy(u'In what priority the tickets will show, higher number will show first.'))
    available_from = models.DateTimeField(_lazy(u'release date'), default=datetime.now, help_text=_lazy(u'When the tickets will be made available'))
    number_of_seats = models.IntegerField(_lazy(u'seats'))

    def number_of_seats_used(self):
        return self.ticket_set.count()

    def is_available(self):
        return datetime.now() >= self.available_from

    def number_of_free_seats(self):
        return self.number_of_seats - self.number_of_seats_used()

    class Meta:
        verbose_name = _lazy(u'ticket type')
        verbose_name_plural = _lazy(u'ticket types')


class TicketTypeTranslation(get_translation_model(TicketType, 'TicketType')):
    title = models.CharField(_lazy(u'title'), max_length=50)
    description = models.TextField(_lazy(u'description'), blank=True)

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = _lazy(u'ticket type translation')
        verbose_name_plural = _lazy(u'ticket type translation')


class Ticket(models.Model):
    user = models.ForeignKey(User, verbose_name=_lazy(u'user'))
    ticket_type = models.ForeignKey(TicketType, verbose_name=_lazy(u'ticket type'))
    bought_date = models.DateField(_lazy(u'bought date'))
    valid = models.BooleanField(_lazy(u'is valid'), default=True)
    invalid_date = models.DateField(_lazy(u'invalid date'), null=True, blank=True)
    invalid_description = models.TextField(_lazy(u'invalid description'), blank=True)

    def __unicode__(self):
        return self.user.username

    class Meta:
        verbose_name = _lazy(u'ticket')
        verbose_name_plural = _lazy(u'tickets')
        index_together = ['user', 'ticket_type']


class Directions(models.Model):
    lan = models.ForeignKey(LAN, verbose_name=_lazy(u'lan'))
    title = models.TextField(_lazy(u'title'))
    description = models.TextField(_lazy(u'description'), blank=True, help_text=_lazy(u'Directions.'))

    class Meta:
        verbose_name = _lazy(u'LAN directions')
        verbose_name_plural = _lazy(u'LAN directions')

    def __unicode__(self):
        return unicode(self.lan) + u' – ' + self.title


class Stream(models.Model):
    title = models.CharField(_lazy(u'title'), max_length=100)
    description = models.TextField(_lazy(u'description'), blank=True)
    link = models.TextField(_lazy(u'link'), help_text=_lazy(u'Embedding link for twitch etc. Include the complete IFrame.'))
    active = models.BooleanField(_lazy(u'is active'), default=False, help_text=_lazy(u'No more than one stream can be active at any given time.'))

    def is_active(self):
        return self.active

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = _lazy(u'stream')
        verbose_name_plural = _lazy(u'streams')
