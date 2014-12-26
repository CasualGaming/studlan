
from django.contrib.auth.models import User
from django.db import models
from apps.lan.models import LAN
from django.db.models import Q
import datetime

class Seating(models.Model):
    lan = models.ForeignKey(LAN)
    title = models.CharField('title', max_length=50)
    desc = models.CharField('desc', max_length=250)
    number_of_seats = models.IntegerField('number of seats')
    closing_date = models.DateTimeField("closing date")

    def save(self, *args, **kwargs):
        if not self.pk:
            super(Seating, self).save(*args, **kwargs)
            self.populate_seats()
        else:
            super(Seating, self).save(*args, **kwargs)

    def get_user_registered(self):
        return map(lambda x: getattr(x, 'user'), Seat.objects.filter(~Q(user=None), Q(seating=self)))

    def get_total_seats(self):
        return Seat.objects.filter(Q(seating=self))

    def get_number_of_seats(self):
        return Seat.objects.filter(Q(seating=self)).count()

    def is_open(self):
        return datetime.datetime.now() < self.closing_date

    def get_free_seats(self):
        total_seats = self.get_total_seats()
        counter = 0
        for seat in total_seats:
            if seat.is_empty():
                counter += 1
        return counter

    def __unicode__(self):
        return self.title

    @models.permalink
    def get_absolute_url(self):
       return ('seating_details', (), {'seating_id': self.id})

    def populate_seats(self):
        for k in range(0,self.number_of_seats):
            seat = Seat(seating=self, placement=k+1)
            seat.save()


class Seat(models.Model):
    user = models.ForeignKey(User, null=True, blank=True)
    seating = models.ForeignKey(Seating)
    placement = models.IntegerField("placement id")

    def __unicode__(self):
        return str(self.id)

    def is_empty(self):
        if self.user is None:
            return True
        else:
            return False