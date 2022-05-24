# -*- coding: utf-8 -*-

from datetime import datetime

from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from apps.userprofile.models import User


class SendMail(models.Model):
    """
    Meta class for the app.
    """

    class Meta:
        managed = False

        permissions = (
            ('list', u'Can list mails'),
            ('send', u'Can send mails'),
        )


class Mail(models.Model):
    """
    A mail sent using the Send-Mail feature.
    """

    uid = models.UUIDField(_(u'ID'), primary_key=True, help_text=_(u'Specified UUID, prevents accidentally sending same mail multiple times.'))
    created_time = models.DateTimeField(_(u'time sent'), default=datetime.now)
    subject = models.CharField(_(u'subject'), max_length=100)
    content = models.TextField(_(u'content'))

    class Meta:
        verbose_name = _(u'mail')
        verbose_name_plural = _(u'mails')
        ordering = ['-created_time']

    def __unicode__(self):
        return '{subject} ({time})'.format(subject=self.subject, time=self.created_time)

    def get_absolute_url(self):
        return reverse('sendmail_mail', kwargs={'id': self.id})

    def recipient_count(self):
        return MailRecipient.objects.filter(mail=self.uid).count()

    def is_sending_complete(self):
        return not MailRecipient.objects.filter(mail=self.uid, sent_time=None).exists()


class MailRecipient(models.Model):
    """
    A recipient of a specific mail.
    """

    mail = models.ForeignKey(Mail, verbose_name=_(u'mail'))
    user = models.ForeignKey(User, verbose_name=_(u'user'))
    sent_time = models.DateTimeField(_(u'time sent'), blank=True, null=True, help_text=_(u'Time the email was sent. Unset if not sent yet.'))

    class Meta:
        verbose_name = _(u'mail recipient')
        verbose_name_plural = _(u'mail recipients')
        ordering = ['-sent_time']

    def __unicode__(self):
        return '{mail_id} ({user})'.format(mail_id=self.mail, user=self.user)
