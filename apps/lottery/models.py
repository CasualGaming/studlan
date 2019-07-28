# -*- coding: utf-8 -*-

from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from translatable.models import TranslatableModel, get_translation_model

from apps.lan.models import LAN


class Lottery(TranslatableModel):
    lan = models.ForeignKey(LAN)
    registration_open = models.BooleanField(_(u'open'), default=False)
    multiple_winnings = models.BooleanField(_(u'multiple winnings'), default=False, help_text=_(u'Allows a user to win more than one time.'))

    def is_participating(self, user):
        for participant in self.lotteryparticipant_set.all():
            if participant.user == user:
                return True

        return False

    def has_won(self, user):
        for winner in self.lotterywinner_set.all():
            if winner.user == user:
                return True

        return False

    def get_absolute_url(self):
        return reverse('details', kwargs={'lottery_id': self.id})

    class Meta:
        verbose_name = _(u'lottery')
        verbose_name_plural = _(u'lotteries')
        permissions = (
            ('draw', 'Can draw winners'),
        )


class LotteryTranslation(get_translation_model(Lottery, 'lottery')):
    title = models.CharField(_(u'title'), max_length=50)
    description = models.TextField(_(u'description'))

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = _(u'lottery translation')
        verbose_name_plural = _(u'lottery translations')


class LotteryParticipant(models.Model):
    lottery = models.ForeignKey(Lottery, verbose_name=_(u'lottery'), editable=False)
    user = models.ForeignKey(User, verbose_name=_(u'user'), editable=False)

    def __unicode__(self):
        return unicode(self.user)

    class Meta:
        verbose_name = _(u'lottery participant')
        verbose_name_plural = _(u'lottery participants')


class LotteryWinner(models.Model):
    lottery = models.ForeignKey(Lottery, verbose_name=_(u'lottery'), editable=False)
    user = models.ForeignKey(User, verbose_name=_(u'user'), editable=False)

    def __unicode__(self):
        return unicode(self.user)

    class Meta:
        verbose_name = _(u'lottery winner')
        verbose_name_plural = _(u'lottery winners')
