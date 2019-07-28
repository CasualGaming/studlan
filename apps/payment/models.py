# -*- coding: utf-8 -*-

from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _

from apps.lan.models import LAN


class Payment(models.Model):
    lan = models.ForeignKey(LAN, verbose_name=_(u'lan'))
    user = models.ForeignKey(User, verbose_name=_(u'user'))
    payed_date = models.DateField(_(u'payed date'))

    valid = models.BooleanField(_(u'is valid'), default=True)
    invalid_date = models.DateField(_(u'invalid date'), null=True, blank=True)

    class Meta:
        verbose_name = _(u'LAN payment')
        verbose_name_plural = _(u'LAN payment')
