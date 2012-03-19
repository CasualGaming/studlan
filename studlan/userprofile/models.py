# -*- coding: utf-8 -*-

from datetime import date

from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save

class UserProfile(models.Model):

    GENDERS = ((1, 'MALE'), (2, 'FEMALE'))

    user = models.OneToOneField(User, editable=False)

    nick = models.CharField('nick', max_length=20, 
        help_text='Specify a nick name (display name).')
    signed_up = models.BooleanField('Signed up')
    has_paid = models.BooleanField('Has payed')
    wants_to_sit_with = models.TextField('Wants to sit with', help_text='Names/nicks of people this user wants to sit with.', blank=True)
    gender = models.SmallIntegerField('Gender', choices=GENDERS, default=1)
    date_of_birth = models.DateField('Date of birth', default=date.today)
    address = models.TextField('Street address')
    zip_code = models.IntegerField('Zip code')
    phone = models.CharField('Phone number', max_length=20)

    def __unicode__(self):
        return self.user.username

    def getMonth(self):
        return ('%02d' % self.date_of_birth.month)

    def getDay(self):
        return ('%02d' % self.date_of_birth.day)

User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User,
                  dispatch_uid='users-profilecreation-signal')
