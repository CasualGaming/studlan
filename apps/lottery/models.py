# -*- coding: utf-8 -*-

from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _lazy

from translatable.models import TranslatableModel, get_translation_model

from apps.lan.models import LAN


class Lottery(TranslatableModel):
    lan = models.ForeignKey(LAN)
    registration_open = models.BooleanField(_lazy(u'open'), default=False)
    multiple_winnings = models.BooleanField(_lazy(u'multiple winnings'), default=False, help_text=_lazy(u'Allows a user to win more than one time.'))

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
        verbose_name = _lazy(u'lottery')
        verbose_name_plural = _lazy(u'lotteries')
        permissions = (
            ('draw', 'Can draw winners'),
        )


class LotteryTranslation(get_translation_model(Lottery, 'lottery')):
    title = models.CharField(_lazy(u'title'), max_length=50)
    description = models.TextField(_lazy(u'description'))

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = _lazy(u'lottery translation')
        verbose_name_plural = _lazy(u'lottery translations')


class LotteryParticipant(models.Model):
    lottery = models.ForeignKey(Lottery, verbose_name=_lazy(u'lottery'), editable=False)
    user = models.ForeignKey(User, verbose_name=_lazy(u'user'), editable=False)

    def __unicode__(self):
        return unicode(self.user)

    class Meta:
        verbose_name = _lazy(u'lottery participant')
        verbose_name_plural = _lazy(u'lottery participants')


class LotteryWinner(models.Model):
    lottery = models.ForeignKey(Lottery, verbose_name=_lazy(u'lottery'), editable=False)
    user = models.ForeignKey(User, verbose_name=_lazy(u'user'), editable=False)

    def __unicode__(self):
        return unicode(self.user)

    class Meta:
        verbose_name = _lazy(u'lottery winner')
        verbose_name_plural = _lazy(u'lottery winners')
