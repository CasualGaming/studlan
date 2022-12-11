# -*- coding: utf-8 -*-

from datetime import datetime

from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _, ugettext_noop


class LAN(models.Model):

    SLUG_REGEX = r'[a-zA-Z][a-zA-Z0-9]*'
    FULL_SLUG_REGEX = r'^' + SLUG_REGEX + r'$'

    MEDIA_TYPE_IMAGE = 'image'
    MEDIA_TYPE_VIDEO = 'video'
    MEDIA_TYPE_STREAM = 'stream'
    MEDIA_TYPES = (
        (MEDIA_TYPE_IMAGE, _('Image')),
        (MEDIA_TYPE_VIDEO, _('Video')),
        (MEDIA_TYPE_STREAM, _('Stream')),
    )

    slug = models.SlugField(
        _('slug'), db_index=True, blank=True, validators=[RegexValidator(regex=FULL_SLUG_REGEX)],
        help_text=_('Optional. Must be alphanumeric and start with a letter.'),
    )
    title = models.CharField(_('title'), max_length=100)
    start_date = models.DateTimeField(_('start date'))
    end_date = models.DateTimeField(_('end date'))
    allow_manual_payment = models.BooleanField(_('allow manual payment'), default=False)
    location = models.CharField(_('location'), max_length=100)
    map_link = models.CharField(_('map link'), max_length=300, help_text=_('URL for an embedded map.'), blank=True)
    media_link = models.CharField(_('media link'), max_length=300, help_text=_('URL for embedded media.'), blank=True)
    media_type = models.CharField(_('media type'), max_length=10, choices=MEDIA_TYPES, default=MEDIA_TYPE_IMAGE, help_text=_('Type of the optional embedded media.'))
    frontpage_media_link = models.CharField(_('frontpage media link'), max_length=300, help_text=_('URL for embedded media on front page.'), blank=True)
    frontpage_media_type = models.CharField(_('frontpage media type'), max_length=10, choices=MEDIA_TYPES, default=MEDIA_TYPE_IMAGE, help_text=_('Type of the optional embedded media on front page.'))
    rules_link = models.CharField(_('rules link'), max_length=300, help_text=_('URL to rules which users have to accept to buy tickets.'), blank=True)
    schedule_link = models.CharField(_('schedule link'), max_length=300, help_text=_('URL to an alternative schedule page.'), blank=True)

    @property
    def attendees(self):
        return [getattr(x, 'user') for x in Attendee.objects.filter(lan=self)]

    @property
    def paid_attendees(self):
        return [getattr(x, 'user') for x in Attendee.objects.filter(lan=self, has_paid=True)]

    def status(self):
        now = datetime.now()
        if now < self.start_date:
            return ugettext_noop('upcoming')
        else:
            if now < self.end_date:
                return ugettext_noop('in progress')
            else:
                return ugettext_noop('ended')

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

    def is_ended(self):
        return self.end_date < datetime.now()

    def get_absolute_url(self):
        if self.slug:
            return reverse('lan_details_slug', kwargs={'lan_slug': self.slug})
        return reverse('lan_details', kwargs={'lan_id': self.id})

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = _('LAN')
        verbose_name_plural = _('LANs')
        ordering = ['start_date']
        permissions = (
            ('export_paying_participants', 'Can export list of paying participants to downloadable file'),
            ('register_arrivals', 'Can show and register arrivals'),
            ('show_arrivals_statistics', 'Can show statistics about arrivals'),
            ('register_new_user', 'Can directly register a new user'),
        )



class Attendee(models.Model):
    user = models.ForeignKey(User, verbose_name=_('user'), on_delete=models.CASCADE)
    lan = models.ForeignKey(LAN, verbose_name=_('LAN'), on_delete=models.CASCADE)
    has_paid = models.BooleanField(_('has paid'), default=False)
    arrived = models.BooleanField(_('has arrived'), default=False)

    def __unicode__(self):
        return self.user.username + ' – ' + self.lan.title

    def get_ticket(self):
        tickets = Ticket.objects.filter(user=self.user, ticket_type__lan=self.lan)
        if tickets:
            # Ignore extra tickets
            return tickets[0]
        return None

    def get_seat(self):
        from apps.seating.models import Seat

        seats = Seat.objects.filter(user=self.user, seating__lan=self.lan)
        if seats:
            # Ignore extra seats
            return seats[0]
        return None

    class Meta:
        verbose_name = _('LAN attendee')
        verbose_name_plural = _('LAN attendees')
        ordering = ['-user', 'lan']
        unique_together = ('user', 'lan')
        index_together = ['user', 'lan']


class TicketType(models.Model):
    # Note: "seats" in this context means "tickets" or "spots", not actual seats.

    lan = models.ForeignKey(LAN, verbose_name=_('LAN'), on_delete=models.CASCADE)
    price = models.IntegerField(_('price'), default=50)
    priority = models.IntegerField(_('priority'), default=0, help_text=_('In what priority the tickets will show, higher number will show first.'))
    available_from = models.DateTimeField(_('release date'), default=datetime.now, help_text=_('When the tickets will be made available.'))
    number_of_seats = models.IntegerField(_('seats'))
    frame_background_color = models.CharField(_('frame background color'), max_length=50, blank=True)
    frame_foreground_color = models.CharField(_('frame foreground color'), max_length=50, blank=True)

    @property
    def verbose_price(self):
        return _('{price}kr').format(price=self.price)

    def number_of_seats_used(self):
        return self.ticket_set.count()

    def is_available(self):
        return datetime.now() >= self.available_from

    def number_of_free_seats(self):
        return self.number_of_seats - self.number_of_seats_used()

    def is_sold_out(self):
        return self.number_of_seats <= self.number_of_seats_used()

    class Meta:
        verbose_name = _('ticket type')
        verbose_name_plural = _('ticket types')




class Ticket(models.Model):
    user = models.ForeignKey(User, verbose_name=_('user'), on_delete=models.CASCADE)
    ticket_type = models.ForeignKey(TicketType, verbose_name=_('ticket type'), on_delete=models.CASCADE)
    bought_date = models.DateField(_('bought date'))
    valid = models.BooleanField(_('is valid'), default=True)
    invalid_date = models.DateField(_('invalid date'), null=True, blank=True)
    invalid_description = models.TextField(_('invalid description'), null=True, blank=True)

    def __unicode__(self):
        return str(self.ticket_type) + ' – ' + self.user.username

    class Meta:
        verbose_name = _('ticket')
        verbose_name_plural = _('tickets')
        index_together = ['user', 'ticket_type']


class Directions(models.Model):
    lan = models.ForeignKey(LAN, verbose_name=_('LAN'), on_delete=models.CASCADE)
    title = models.CharField(_('title'), max_length=100, null=True)
    description = models.TextField(_('description'), null=True, blank=True, help_text=_('Directions.'))

    class Meta:
        verbose_name = _('LAN directions')
        verbose_name_plural = _('LAN directions')

    def __unicode__(self):
        return str(self.lan) + ' – ' + self.title


class Stream(models.Model):
    title = models.CharField(_('title'), max_length=100)
    visible_title = models.CharField(_('visible title'), max_length=100, blank=True, help_text=_('Title to show above stream. May be empty.'))
    description = models.TextField(_('description'), blank=True, help_text=_('Short description that will show on front page.'))
    link = models.CharField(_('link'), max_length=300, help_text=_('Link to the embedding stream.'))
    active = models.BooleanField(_('is active'), default=False, help_text=_('No more than one stream can be active at any given time.'))

    def is_active(self):
        return self.active

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = _('stream')
        verbose_name_plural = _('streams')
