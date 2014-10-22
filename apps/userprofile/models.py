# -*- coding: utf-8 -*-

from datetime import date

from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
    
GENDERS = ((1, 'Male'), (2, 'Female'))

class UserProfile(models.Model):

    user = models.ForeignKey(User, unique=True)

    nick = models.CharField('nick', max_length=20, 
        help_text='Specify a nick name (display name).')
    wants_to_sit_with = models.TextField('Wants to sit with', help_text='Names/nicks of people this user wants to sit with.', blank=True)
    gender = models.SmallIntegerField('Gender', choices=GENDERS, default=1)
    date_of_birth = models.DateField('Date of birth', default=date.today)
    address = models.CharField('Street address', max_length=100)
    zip_code = models.CharField('Zip code', max_length=4)
    phone = models.CharField('Phone number', max_length=20)
    ntnu_username = models.CharField('NTNU username', max_length=20, blank=True, null=True)

    def __unicode__(self):
        return self.user.username

    def getMonth(self):
        return ('%02d' % self.date_of_birth.month)

    def getDay(self):
        return ('%02d' % self.date_of_birth.day)

    def has_address(self):
        if self.address and self.zip_code:
            if not self.address.strip() or not self.zip_code.strip():
                return False
            return True
        return False

User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])
