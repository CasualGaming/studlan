# -*- coding: utf-8 -*-

from datetime import date

from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _


class UserProfile(models.Model):
    user = models.OneToOneField(User, verbose_name=_(u'user'), related_name='profile')
    nick = models.CharField(_(u'nick'), max_length=20, help_text=_(u'Specify a nick name (display name).'), db_index=True)
    date_of_birth = models.DateField(_(u'date of birth'), default=date.today)
    address = models.CharField(_(u'street address'), max_length=100)
    zip_code = models.CharField(_(u'postal code'), max_length=4)
    phone = models.CharField(_(u'phone number'), max_length=20)

    def __unicode__(self):
        return self.user.username

    def get_month(self):
        return u'{0:02d}'.format(self.date_of_birth.month)

    def get_day(self):
        return u'{0:02d}'.format(self.date_of_birth.day)

    def has_address(self):
        if self.address and self.zip_code:
            if not self.address.strip() or not self.zip_code.strip():
                return False
            return True
        return False

    class Meta:
        verbose_name = _(u'user profile')
        verbose_name_plural = _(u'user profiles')
        permissions = (
            ('show_private_info', u'Can show private user info'),
        )


User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])


class AliasType(models.Model):
    description = models.CharField(_(u'description'), max_length=100)
    profile_url = models.URLField(_(u'profile URL'), blank=True, null=True, help_text=_(u'URL prefix where profile info can be '
                                  'retrieved. E.g. https://steamcommunity.com/id/'))
    activity = models.ManyToManyField('competition.Activity', verbose_name=_(u'activity'), related_name='alias_type')

    def __unicode__(self):
        return self.description

    class Meta:
        verbose_name = _(u'user alias type')
        verbose_name_plural = _(u'user alias types')


class Alias(models.Model):
    alias_type = models.ForeignKey(AliasType, verbose_name=_(u'alias type'))
    nick = models.CharField(_(u'nickname'), max_length=40)
    user = models.ForeignKey(User, verbose_name=_(u'user'), related_name='alias')

    def __unicode__(self):
        return self.nick

    class Meta:
        verbose_name = _(u'user alias')
        verbose_name_plural = _(u'user aliases')
        unique_together = ('user', 'alias_type')
