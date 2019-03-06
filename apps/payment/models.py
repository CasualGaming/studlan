# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User

from apps.lan.models import LAN


class Payment(models.Model):
    lan = models.ForeignKey(LAN)
    user = models.ForeignKey(User)
    payed_date = models.DateField()

    valid = models.BooleanField(default=True)
    invalid_date = models.DateField(null=True, blank=True)
