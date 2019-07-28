# -*- coding: utf-8 -*-

from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext as _, ugettext_lazy as _lazy


class Key(models.Model):
    content = models.CharField(_lazy(u'key'), max_length=32, editable=False)
    owner = models.ForeignKey(User)

    def __unicode__(self):
        return _(u'API key for %(owner)s') % self.owner

    class Meta:
        verbose_name = _lazy(u'API key')
        verbose_name_plural = _lazy(u'API keys')
