# -*- coding: utf-8 -*-

import datetime

from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _


class RegisterToken(models.Model):
    user = models.ForeignKey(User)
    token = models.CharField(_(u'token'), max_length=32)
    created = models.DateTimeField(_(u'created'), editable=False, auto_now_add=True)

    @property
    def is_valid(self):
        valid_period = datetime.timedelta(days=1)
        now = datetime.datetime.now()
        return now < self.created + valid_period

    class Meta:
        verbose_name = _(u'register token')
        verbose_name_plural = _(u'register tokens')
