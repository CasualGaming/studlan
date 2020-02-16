# -*- coding: utf-8 -*-

from datetime import datetime

from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from apps.competition.models import Competition
from apps.lan.models import LAN, TicketType
from apps.team.models import Team
from apps.userprofile.models import User


class SendMail(models.Model):
    """
    Meta class for the app.
    """

    class Meta:
        managed = False

        permissions = (
            ('send_mail', u'Can send mails to users'),
        )


class Mail(models.Model):
    """
    A mail sent using the Send-Mail feature.
    """

    form_id = models.UUIDField(_(u'form id'), null=True, blank=True, help_text=_(u'To prevent sending the same mail twice.'))
    sent_time = models.DateTimeField(_(u'time sent'), default=datetime.now)
    subject = models.CharField(_(u'subject'), max_length=80)
    content = models.TextField(_(u'content'))
    recipient_everyone = models.BooleanField(_(u'recipient everyone'), default=False, help_text=_(u'Pinned articles are shown before non-pinned ones.'))
    recipient_lans = models.ManyToManyField(LAN, verbose_name=_(u'recipient LANs'), blank=True)
    recipient_tickets = models.ManyToManyField(TicketType, verbose_name=_(u'recipient tickets'), blank=True)
    recipient_teams = models.ManyToManyField(Team, verbose_name=_(u'recipient teams'), blank=True)
    recipient_competitions = models.ManyToManyField(Competition, verbose_name=_(u'recipient competitions'), blank=True)
    recipient_users = models.ManyToManyField(User, verbose_name=_(u'recipient users'), blank=True)
    recipients_total = models.IntegerField(_(u'total number of recipients'), default=0, help_text=_(u'Sum of all unique users that should receive the mail.'))
    successful_mails = models.IntegerField(_(u'successful mails'), default=0, help_text=_(u'How many of the mails were sent successfully.'))
    failed_mails = models.IntegerField(_(u'failed mails'), default=0, help_text=_(u'How many of the mails were not sent because of some failure.'))
    done_sending = models.BooleanField(_(u'done sending'), default=False, help_text=_(u'If all mails have been attempted sent.'))

    class Meta:
        verbose_name = _(u'mail')
        verbose_name_plural = _(u'mails')
        ordering = ['-sent_time']

    def __unicode__(self):
        return self.subject

    def get_absolute_url(self):
        return reverse('sendmail_mail', kwargs={'id': self.id})
