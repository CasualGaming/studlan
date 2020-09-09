# -*- coding: utf-8 -*-

from datetime import datetime

from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _, ugettext_noop

from translatable.models import TranslatableModel, get_translation_model


class LAN(TranslatableModel):

    SLUG_REGEX = r'[a-zA-Z][a-zA-Z0-9]*'
    FULL_SLUG_REGEX = r'^' + SLUG_REGEX + r'$'

    MEDIA_TYPE_IMAGE = 'image'
    MEDIA_TYPE_VIDEO = 'video'
    MEDIA_TYPE_STREAM = 'stream'
    MEDIA_TYPES = (
        (MEDIA_TYPE_IMAGE, _(u'Image')),
        (MEDIA_TYPE_VIDEO, _(u'Video')),
        (MEDIA_TYPE_STREAM, _(u'Stream')),
    )

    slug = models.SlugField(
        _(u'slug'), db_index=True, blank=True, validators=[RegexValidator(regex=FULL_SLUG_REGEX)],
        help_text=_(u'Optional. Must be alphanumeric and start with a letter.'),
    )
    title = models.CharField(_(u'title'), max_length=100)
    start_date = models.DateTimeField(_(u'start date'))
    end_date = models.DateTimeField(_(u'end date'))
    allow_manual_payment = models.BooleanField(_(u'allow manual payment'), default=False)
    location = models.CharField(_(u'location'), max_length=100)
    map_link = models.CharField(_(u'map link'), max_length=300, help_text=_(u'URL for an embedded map.'), blank=True)
    media_link = models.CharField(_(u'media link'), max_length=300, help_text=_(u'URL for embedded media.'), blank=True)
    media_type = models.CharField(_(u'media type'), max_length=10, choices=MEDIA_TYPES, default=MEDIA_TYPE_IMAGE, help_text=_(u'Type of the optional embedded media.'))
    frontpage_media_link = models.CharField(_(u'frontpage media link'), max_length=300, help_text=_(u'URL for embedded media on front page.'), blank=True)
    frontpage_media_type = models.CharField(_(u'frontpage media type'), max_length=10, choices=MEDIA_TYPES, default=MEDIA_TYPE_IMAGE, help_text=_(u'Type of the optional embedded media on front page.'))

    @property
    def attendees(self):
        return map(lambda x: getattr(x, 'user'), Attendee.objects.filter(lan=self))

    @property
    def paid_attendees(self):
        return map(lambda x: getattr(x, 'user'), Attendee.objects.filter(lan=self, has_paid=True))

    def status(self):
        now = datetime.now()
        if now < self.start_date:
            return ugettext_noop(u'upcoming')
        else:
            if now < self.end_date:
                return ugettext_noop(u'in progress')
            else:
                return ugettext_noop(u'ended')

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
        verbose_name = _(u'LAN')
        verbose_name_plural = _(u'LANs')
        ordering = ['start_date']
        permissions = (
            ('export_paying_participants', u'Can export list of paying participants to downloadable file'),
            ('register_arrivals', u'Can show and register arrivals'),
            ('show_arrivals_statistics', u'Can show statistics about arrivals'),
            ('register_new_user', u'Can directly register a new user'),
        )


class LANTranslation(get_translation_model(LAN, 'LAN')):
    description = models.TextField(_(u'description'))

    class Meta:
        verbose_name = _(u'LAN translation')
        verbose_name_plural = _(u'LAN translations')


class Attendee(models.Model):
    user = models.ForeignKey(User, verbose_name=_(u'user'))
    lan = models.ForeignKey(LAN, verbose_name=_(u'LAN'))
    has_paid = models.BooleanField(_(u'has paid'), default=False)
    arrived = models.BooleanField(_(u'has arrived'), default=False)

    def __unicode__(self):
        return self.user.username + u' – ' + self.lan.title

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
        verbose_name = _(u'LAN attendee')
        verbose_name_plural = _(u'LAN attendees')
        ordering = ['-user', 'lan']
        unique_together = ('user', 'lan')
        index_together = ['user', 'lan']


class TicketType(TranslatableModel):
    # Note: "seats" in this context means "tickets" or "spots", not actual seats.

    lan = models.ForeignKey(LAN, verbose_name=_(u'LAN'))
    price = models.IntegerField(_(u'price'), default=50)
    priority = models.IntegerField(_(u'prioity'), default=0, help_text=_(u'In what priority the tickets will show, higher number will show first.'))
    available_from = models.DateTimeField(_(u'release date'), default=datetime.now, help_text=_(u'When the tickets will be made available.'))
    number_of_seats = models.IntegerField(_(u'seats'))

    @property
    def verbose_price(self):
        return _(u'{price}kr').format(price=self.price)

    def number_of_seats_used(self):
        return self.ticket_set.count()

    def is_available(self):
        return datetime.now() >= self.available_from

    def number_of_free_seats(self):
        return self.number_of_seats - self.number_of_seats_used()

    def is_sold_out(self):
        return self.number_of_seats <= self.number_of_seats_used()

    class Meta:
        verbose_name = _(u'ticket type')
        verbose_name_plural = _(u'ticket types')


class TicketTypeTranslation(get_translation_model(TicketType, 'TicketType')):
    title = models.CharField(_(u'title'), max_length=50)
    description = models.TextField(_(u'description'), blank=True)

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = _(u'ticket type translation')
        verbose_name_plural = _(u'ticket type translation')


class Ticket(models.Model):
    user = models.ForeignKey(User, verbose_name=_(u'user'))
    ticket_type = models.ForeignKey(TicketType, verbose_name=_(u'ticket type'))
    bought_date = models.DateField(_(u'bought date'))
    valid = models.BooleanField(_(u'is valid'), default=True)
    invalid_date = models.DateField(_(u'invalid date'), null=True, blank=True)
    invalid_description = models.TextField(_(u'invalid description'), null=True, blank=True)

    def __unicode__(self):
        return unicode(self.ticket_type) + u' – ' + self.user.username

    class Meta:
        verbose_name = _(u'ticket')
        verbose_name_plural = _(u'tickets')
        index_together = ['user', 'ticket_type']


class Directions(models.Model):
    lan = models.ForeignKey(LAN, verbose_name=_(u'LAN'))
    title = models.CharField(_(u'title'), max_length=100, null=True)
    description = models.TextField(_(u'description'), null=True, blank=True, help_text=_(u'Directions.'))

    class Meta:
        verbose_name = _(u'LAN directions')
        verbose_name_plural = _(u'LAN directions')

    def __unicode__(self):
        return unicode(self.lan) + u' – ' + self.title


class Stream(models.Model):
    title = models.CharField(_(u'title'), max_length=100)
    visible_title = models.CharField(_(u'visible title'), max_length=100, blank=True, help_text=_(u'Title to show above stream. May be empty.'))
    description = models.TextField(_(u'description'), blank=True, help_text=_(u'Short description that will show on front page.'))
    link = models.CharField(_(u'link'), max_length=300, help_text=_(u'Link to the embedding stream.'))
    active = models.BooleanField(_(u'is active'), default=False, help_text=_(u'No more than one stream can be active at any given time.'))

    def is_active(self):
        return self.active

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = _(u'stream')
        verbose_name_plural = _(u'streams')
