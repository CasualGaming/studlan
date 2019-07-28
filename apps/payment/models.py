# -*- coding: utf-8 -*-

from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _lazy

from apps.lan.models import LAN


class Payment(models.Model):
    lan = models.ForeignKey(LAN, verbose_name=_lazy(u'lan'))
    user = models.ForeignKey(User, verbose_name=_lazy(u'user'))
    payed_date = models.DateField(_lazy(u'payed date'))

    valid = models.BooleanField(_lazy(u'is valid'), default=True)
    invalid_date = models.DateField(_lazy(u'invalid date'), null=True, blank=True)

    class Meta:
        verbose_name = _lazy(u'LAN payment')
        verbose_name_plural = _lazy(u'LAN payment')
