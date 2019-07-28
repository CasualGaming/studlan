# -*- coding: utf-8 -*-

from datetime import date

from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _lazy


class UserProfile(models.Model):
    user = models.OneToOneField(User, verbose_name=_lazy(u'user'), related_name='profile')
    nick = models.CharField(_lazy(u'nick'), max_length=20, help_text=_lazy(u'Specify a nick name (display name).'), db_index=True)
    date_of_birth = models.DateField(_lazy(u'date of birth'), default=date.today)
    address = models.CharField(_lazy(u'street address'), max_length=100)
    zip_code = models.CharField(_lazy(u'zip code'), max_length=4)
    phone = models.CharField(_lazy(u'phone number'), max_length=20)

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
        verbose_name = _lazy(u'user profile')
        verbose_name_plural = _lazy(u'user profiles')
        permissions = (
            ('show_private_info', 'Can show private user info'),
        )


User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])


class AliasType(models.Model):
    description = models.CharField(_lazy(u'description'), max_length=100)
    profile_url = models.URLField(_lazy(u'profile URL'), blank=True, null=True, help_text=_lazy(u'URL prefix where profile info can be '
                                  'retrieved. E.g. https://steamcommunity.com/id/'))
    activity = models.ManyToManyField('competition.Activity', verbose_name=_lazy(u'activity'), related_name='alias_type')

    def __unicode__(self):
        return self.description

    class Meta:
        verbose_name = _lazy(u'user alias type')
        verbose_name_plural = _lazy(u'user alias types')


class Alias(models.Model):
    alias_type = models.ForeignKey(AliasType, verbose_name=_lazy(u'alias type'))
    nick = models.CharField(_lazy(u'nickname'), max_length=40)
    user = models.ForeignKey(User, verbose_name=_lazy(u'user'), related_name='alias')

    def __unicode__(self):
        return self.nick

    class Meta:
        verbose_name = _lazy(u'user alias')
        verbose_name_plural = _lazy(u'user aliases')
        unique_together = ('user', 'alias_type')
