# -*- coding: utf-8 -*-

from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from apps.lan.models import LAN


class Poll(models.Model):
    lan = models.ForeignKey(LAN, verbose_name=_(u'LAN'), on_delete=models.CASCADE)
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



class PollOption(models.Model):
    poll = models.ForeignKey(Poll, verbose_name=_(u'poll'), editable=False, on_delete=models.CASCADE)
    value = models.CharField(_(u'value'), max_length=50)

    def __unicode__(self):
        return unicode(self.value)

    class Meta:
        verbose_name = _(u'poll option')
        verbose_name_plural = _(u'poll options')


class PollParticipant(models.Model):
    poll = models.ForeignKey(Poll, verbose_name=_(u'poll'), on_delete=models.CASCADE)
    user = models.ForeignKey(User, verbose_name=_(u'user'), on_delete=models.CASCADE)
    option = models.ForeignKey(PollOption, verbose_name=_(u'option'), on_delete=models.CASCADE)

    def __unicode__(self):
        return unicode(self.user)

    class Meta:
        verbose_name = _(u'poll participant')
        verbose_name_plural = _(u'poll participants')
