# -*- coding: utf-8 -*-

from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from apps.lan.models import LAN


class Lottery(models.Model):
    lan = models.ForeignKey(LAN, verbose_name=_(u'LAN'), on_delete=models.CASCADE)
    registration_open = models.BooleanField(_(u'open'), default=False)
    multiple_winnings = models.BooleanField(_(u'multiple winnings'), default=False, help_text=_(u'Allows a user to win more than one time.'))
    enforce_payment = models.BooleanField(_(u'enforce payment'), default=False, help_text=_(u'Require users to have paid for the LAN in order to participate.'))

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
        return reverse('lottery_details', kwargs={'lottery_id': self.id})

    class Meta:
        verbose_name = _(u'lottery')
        verbose_name_plural = _(u'lotteries')
        permissions = (
            ('draw', u'Can draw winners'),
            ('open_close', u'Can open and close lotteries'),
        )




class LotteryParticipant(models.Model):
    lottery = models.ForeignKey(Lottery, verbose_name=_(u'lottery'), editable=False, on_delete=models.CASCADE)
    user = models.ForeignKey(User, verbose_name=_(u'user'), editable=False, on_delete=models.CASCADE)

    def __unicode__(self):
        return unicode(self.user)

    class Meta:
        verbose_name = _(u'lottery participant')
        verbose_name_plural = _(u'lottery participants')


class LotteryWinner(models.Model):
    lottery = models.ForeignKey(Lottery, verbose_name=_(u'lottery'), editable=False, on_delete=models.CASCADE)
    user = models.ForeignKey(User, verbose_name=_(u'user'), editable=False, on_delete=models.CASCADE)

    def __unicode__(self):
        return unicode(self.user)

    class Meta:
        verbose_name = _(u'lottery winner')
        verbose_name_plural = _(u'lottery winners')
