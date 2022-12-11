# -*- coding: utf-8 -*-

from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from apps.lan.models import LAN


class Poll(models.Model):
    lan = models.ForeignKey(LAN, verbose_name=_('LAN'), on_delete=models.CASCADE)
    is_open = models.BooleanField(_('open'), default=False)
    enforce_payment = models.BooleanField(_('enforce payment'), default=False, help_text=_('Require users to have paid for the LAN in order to vote.'))

    def get_absolute_url(self):
        return reverse('poll_details', kwargs={'poll_id': self.id})

    class Meta:
        verbose_name = _('poll')
        verbose_name_plural = _('polls')
        permissions = (
            ('open_close', 'Can open and close polls'),
        )



class PollOption(models.Model):
    poll = models.ForeignKey(Poll, verbose_name=_('poll'), editable=False, on_delete=models.CASCADE)
    value = models.CharField(_('value'), max_length=50)

    def __unicode__(self):
        return str(self.value)

    class Meta:
        verbose_name = _('poll option')
        verbose_name_plural = _('poll options')


class PollParticipant(models.Model):
    poll = models.ForeignKey(Poll, verbose_name=_('poll'), on_delete=models.CASCADE)
    user = models.ForeignKey(User, verbose_name=_('user'), on_delete=models.CASCADE)
    option = models.ForeignKey(PollOption, verbose_name=_('option'), on_delete=models.CASCADE)

    def __unicode__(self):
        return str(self.user)

    class Meta:
        verbose_name = _('poll participant')
        verbose_name_plural = _('poll participants')
