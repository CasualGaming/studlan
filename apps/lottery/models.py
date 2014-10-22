# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User
from translatable.models import TranslatableModel, get_translation_model

from apps.lan.models import LAN, Attendee

class Lottery(TranslatableModel):
    lan = models.ForeignKey(LAN)
    registration_open = models.BooleanField('Open', default=False)
    multiple_winnings = models.BooleanField('Multiple winnings', default=False, help_text='Allows a user to win more than one price')

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

    class Meta:
        verbose_name_plural = "Lotteries"


class LotteryTranslation(get_translation_model(Lottery, 'lottery')):
    title = models.CharField('title', max_length=50)
    description = models.TextField('description')

    def __unicode__(self):
        return self.title


class LotteryParticipant(models.Model):
    lottery = models.ForeignKey(Lottery)
    user = models.ForeignKey(User)
    has_won = models.BooleanField('has won')
    
    def __unicode__(self):
        return unicode(self.user)

class LotteryWinner(models.Model):
    lottery = models.ForeignKey(Lottery)
    user = models.ForeignKey(User)
    
    def __unicode__(self):
        return unicode(self.user)
