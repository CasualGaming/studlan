# -*- coding: utf-8 -*-

from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from translatable.models import TranslatableModel, get_translation_model

from apps.lan.models import LAN


class Poll(TranslatableModel):
    lan = models.ForeignKey(LAN, verbose_name=_(u'LAN'))
    is_open = models.BooleanField(_(u'open'), default=False)
    enforce_payment = models.BooleanField(_(u'enforce payment'), default=False, help_text=_(u'Require users to have paid for the LAN in order to vote.'))

    def get_absolute_url(self):
        return reverse('poll_details', kwargs={'poll_id': self.id})

    class Meta:
        verbose_name = _(u'poll')
        verbose_name_plural = _(u'polls')
        permissions = (
            ('open_close', u'Can open and close polls'),
        )


class PollTranslation(get_translation_model(Poll, 'poll')):
    title = models.CharField(_(u'title'), max_length=50)
    description = models.TextField(_(u'description'))

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = _(u'poll translation')
        verbose_name_plural = _(u'poll translations')


class PollOption(models.Model):
    poll = models.ForeignKey(Poll, verbose_name=_(u'poll'), editable=False)
    value = models.CharField(_(u'value'), max_length=50)

    def __unicode__(self):
        return unicode(self.value)

    class Meta:
        verbose_name = _(u'poll option')
        verbose_name_plural = _(u'poll options')


class PollParticipant(models.Model):
    poll = models.ForeignKey(Poll, verbose_name=_(u'poll'))
    user = models.ForeignKey(User, verbose_name=_(u'user'))
    option = models.ForeignKey(PollOption, verbose_name=_(u'option'))

    def __unicode__(self):
        return unicode(self.user)

    class Meta:
        verbose_name = _(u'poll participant')
        verbose_name_plural = _(u'poll participants')
