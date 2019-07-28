# -*- coding: utf-8 -*-

from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext, ugettext_lazy as _


class Key(models.Model):
    content = models.CharField(_(u'key'), max_length=32, editable=False)
    owner = models.ForeignKey(User)

    def __unicode__(self):
        return ugettext(u'API key for {owner}').format(owner=self.owner)

    class Meta:
        verbose_name = _(u'API key')
        verbose_name_plural = _(u'API keys')
