# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _

from apps.lan.models import LAN


class LANTicketPurchaseLock(models.Model):
    lan = models.OneToOneField(LAN, verbose_name=_(u'lan'), related_name='ticket_purchase_lock')

    class Meta:
        verbose_name = _(u'LAN ticket purchase lock')
        verbose_name_plural = _(u'LAN ticket purchase locks')

    def __unicode__(self):
        return self.lan.title

    def evaluate(self):
        """Convenience method to dereference/fetch from queryset."""
        pass
