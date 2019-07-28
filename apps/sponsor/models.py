# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext_lazy as _lazy

from translatable.models import TranslatableModel, get_translation_model

from apps.lan.models import LAN


class Sponsor(TranslatableModel):
    title = models.CharField(_lazy(u'name'), max_length=50)
    banner = models.CharField(_lazy(u'banner URL'), max_length=100, blank=True,
                              help_text=_lazy(u'Use a mirrored image of at least a height of 150px.'))
    website = models.URLField(_lazy(u'website'), max_length=200)

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = _lazy(u'sponsor')
        verbose_name_plural = _lazy(u'sponsors')


class SponsorTranslation(get_translation_model(Sponsor, 'Sponsor')):
    description = models.TextField(_lazy(u'description'))

    class Meta:
        verbose_name = _lazy(u'sponsor translation')
        verbose_name_plural = _lazy(u'sponsor translations')


class SponsorRelation(models.Model):
    lan = models.ForeignKey(LAN, verbose_name=_lazy(u'lan'))
    sponsor = models.ForeignKey(Sponsor, verbose_name=_lazy(u'sponsor'))
    priority = models.IntegerField(_lazy(u'priority'),
                                   help_text=_lazy(u'higher priority means closer to the top of the sponsor list.'))

    def __unicode__(self):
        return unicode(self.lan) + u' – ' + unicode(self.sponsor)

    class Meta:
        verbose_name = _lazy(u'sponsor relation')
        verbose_name_plural = _lazy(u'sponsor relations')
        ordering = ['-priority']
