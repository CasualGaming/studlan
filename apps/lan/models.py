# -*- coding: utf-8 -*-

from datetime import datetime

from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse

from translatable.models import TranslatableModel, get_translation_model


class LAN(TranslatableModel):
    title = models.CharField('title', max_length=100)
    start_date = models.DateTimeField('start date')
    end_date = models.DateTimeField('end date')
    location = models.CharField('location', max_length=100)
    map_link = models.CharField('map link', max_length=300, help_text='url for google maps embedded map', null=True)

    @property
    def attendees(self):
        return map(lambda x: getattr(x, 'user'), Attendee.objects.filter(lan=self))

    @property
    def paid_attendees(self):
        return map(lambda x: getattr(x, 'user'), Attendee.objects.filter(lan=self, has_paid=True))

    def status(self):
        now = datetime.now()
        if now < self.start_date:
            return 'upcoming'
        else:
            if now < self.end_date:
                return 'in progress'
            else:
                return 'ended'

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
        ordering = ['start_date']
        permissions = (
            ('export_paying_participants', 'Can export list of paying participants to downloadable file'),
            ('register_arrivals', 'Can register arrivals'),
            ('register_new_user', 'Can directly register a new user'),
        )


class LANTranslation(get_translation_model(LAN, 'LAN')):
    description = models.TextField('description')


class Attendee(models.Model):
    user = models.ForeignKey(User)
    lan = models.ForeignKey(LAN)
    has_paid = models.BooleanField('has paid', default=False)
    arrived = models.BooleanField('has arrived', default=False)

    def __unicode__(self):
        return self.user.username + ' – ' + self.lan.title

    class Meta:
        ordering = ['-user', 'lan']
        unique_together = ('user', 'lan')
        index_together = ['user', 'lan']


class TicketType(TranslatableModel):
    lan = models.ForeignKey(LAN)

    price = models.IntegerField('Price', default=50)
    priority = models.IntegerField('Prioity', default=0, help_text='In what priority the tickets will show, '
                                                                   'higher number will show first.')
    available_from = models.DateTimeField('release date', default=datetime.now, help_text='When the tickets will be '
                                                                                          'made available', null=False)
    number_of_seats = models.IntegerField('Seats')

    def number_of_seats_used(self):
        return self.ticket_set.count()

    def is_available(self):
        return datetime.now() >= self.available_from

    def number_of_free_seats(self):
        return self.number_of_seats - self.number_of_seats_used()


class TicketTypeTranslation(get_translation_model(TicketType, 'TicketType')):
    title = models.CharField('Title', max_length=50)
    description = models.TextField('Description', null=True, blank=True)

    def __unicode__(self):
        return self.title


class Ticket(models.Model):
    user = models.ForeignKey(User)
    ticket_type = models.ForeignKey(TicketType)

    bought_date = models.DateField()

    valid = models.BooleanField(default=True)
    invalid_date = models.DateField(null=True, blank=True)
    invalid_description = models.TextField(null=True, blank=True)

    def __unicode__(self):
        return self.user.username

    class Meta:
        index_together = ['user', 'ticket_type']


class Directions(models.Model):
    lan = models.ForeignKey(LAN)
    title = models.TextField('title', null=True)
    description = models.TextField('directions', null=True)

    def __unicode__(self):
        return ' direction ' + str(self.pk)


class Stream(models.Model):
    title = models.CharField('title', max_length=100)
    description = models.TextField('description', help_text='Short description that will show on front page.')
    link = models.TextField('link', help_text='Embedding link for twitch etc. Include the complete IFrame.')
    active = models.BooleanField(default=False, help_text='No more than one stream can be active at any given time.')

    def is_active(self):
        return self.active

    def __unicode__(self):
        return self.title
