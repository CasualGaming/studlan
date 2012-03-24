# -*- coding: utf-8 -*-

from django.contrib.auth.models import User
from django.db import models

class RegisterToken(models.Model):
    user = models.ForeignKey(User)
    token = models.CharField("token", max_length=32)
