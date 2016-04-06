# -*- coding: utf-8 -*-

from datetime import date

from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext as _

GENDERS = ((1, _(u'Male')), (2, _(u'Female')))


class UserProfile(models.Model):

    user = models.ForeignKey(User, related_name='profile', unique=True)

    nick = models.CharField(_(u'nick'), max_length=20, 
        help_text='Specify a nick name (display name).')
    wants_to_sit_with = models.TextField('Wants to sit with', help_text='Names/nicks of people this user wants to sit with.', blank=True)
    gender = models.SmallIntegerField(_(u'Gender'), choices=GENDERS, default=1, blank=True)
    date_of_birth = models.DateField(_(u'Date of birth'), default=date.today)
    address = models.CharField(_(u'Street address'), max_length=100)
    zip_code = models.CharField(_(u'Zip code'), max_length=4)
    phone = models.CharField(_(u'Phone number'), max_length=20)
    ntnu_username = models.CharField(_(u'NTNU username'), max_length=20, blank=True, null=True)

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


class AliasType(models.Model):
    description = models.CharField('Description', max_length=100, help_text='Short description')
    profile_url = models.URLField('Profile url', blank=True, null=True, help_text='Url where profile info can be '
                                  'retrieved. E.g. https://steamcommunity.com/id/')
    activity = models.ForeignKey('competition.Activity', related_name='alias_type', unique=True)

    def __unicode__(self):
        return self.description


class Alias(models.Model):
    alias_type = models.ForeignKey(AliasType)
    nick = models.CharField('nick', max_length=20)
    user = models.ForeignKey(User, related_name='alias')

    def __unicode__(self):
        return self.nick

    class Meta:
        unique_together = ("user", "alias_type")
