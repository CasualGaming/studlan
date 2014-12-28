# -*- coding: utf-8 -*-

from datetime import datetime

from django.contrib.auth.models import User
from django.db import models

from apps.userprofile.models import UserProfile


class LAN(models.Model):
    title = models.CharField("title", max_length=100)
    start_date = models.DateTimeField("start date")
    end_date = models.DateTimeField("end date")
    location = models.CharField("location", max_length=100)
    description = models.TextField("description")

    @property
    def attendees(self):
        return map(lambda x: getattr(x, 'user'), Attendee.objects.filter(lan=self))

    @property
    def paid_attendees(self):
        return map(lambda x: getattr(x, 'user'), Attendee.objects.filter(lan=self, has_paid=True))

    @property
    def attendee_ntnu_usernames(self):
        ntnu = []
        for attendee in self.attendees:
            up_tuple = UserProfile.objects.get_or_create(user=attendee)
            # If True, the userprofile was just created.
            if up_tuple[1]:
                continue
            else:
                ntnu_username = up_tuple[0].ntnu_username
                # If the ntnu_username is only whitespace.
                if not ntnu_username or not ntnu_username.strip():
                    continue
                else:
                    ntnu.append(ntnu_username)

        return ntnu

        # This does the same, but ugly =/
        # return map(lambda x: getattr(UserProfile.objects.get_or_create(user=x)[0], 'ntnu_username'), self.attendees)

    def status(self):
        now = datetime.now()
        if now < self.start_date:
            return 'upcoming'
        else:
            if now < self.end_date:
                return 'in progress'
            else:
                return 'ended'

    @models.permalink
    def get_absolute_url(self):
        return 'lan_details', (), {'lan_id': self.id}

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ['start_date']


class Attendee(models.Model):
    user = models.ForeignKey(User)
    lan = models.ForeignKey(LAN)
    has_paid = models.BooleanField("has paid", default=False)
    arrived = models.BooleanField("has arrived", default=False)

    def __unicode__(self):
        return self.user.get_full_name() + " - " + self.lan.title

    class Meta:
        ordering = ['-user', 'lan', ]


class TicketType(models.Model):
    lan = models.ForeignKey(LAN)

    title = models.CharField("Title", max_length=50)
    price = models.IntegerField("Price", default=50)
    number_of_seats = models.IntegerField("Seats")
    description = models.TextField("Description", null=True, blank=True)

    def __unicode__(self):
        return self.title

    def number_of_seats_used(self):
        return self.ticket_set.count()

    def number_of_free_seats(self):
        return self.number_of_seats - self.number_of_seats_used()

class Ticket(models.Model):
    user = models.ForeignKey(User)
    ticket_type = models.ForeignKey(TicketType)

    bought_date = models.DateField()

    valid = models.BooleanField(default=True)
    invalid_date = models.DateField(null=True, blank=True)
    invalid_description = models.TextField(null=True, blank=True)

