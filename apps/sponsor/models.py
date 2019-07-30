# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext_lazy as _

from translatable.models import TranslatableModel, get_translation_model

from apps.lan.models import LAN


class Sponsor(TranslatableModel):
    title = models.CharField(_(u'name'), max_length=50)
    banner = models.CharField(_(u'banner URL'), max_length=100, blank=True,
                              help_text=_(u'Use a mirrored image of at least a height of 150px.'))
    website = models.URLField(_(u'website'), max_length=200)

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = _(u'sponsor')
        verbose_name_plural = _(u'sponsors')


class SponsorTranslation(get_translation_model(Sponsor, 'Sponsor')):
    description = models.TextField(_(u'description'))

    class Meta:
        verbose_name = _(u'sponsor translation')
        verbose_name_plural = _(u'sponsor translations')


class SponsorRelation(models.Model):
    lan = models.ForeignKey(LAN, verbose_name=_(u'LAN'))
    sponsor = models.ForeignKey(Sponsor, verbose_name=_(u'sponsor'))
    priority = models.IntegerField(_(u'priority'),
                                   help_text=_(u'Higher priority means closer to the top of the sponsor list.'))

    def __unicode__(self):
        return unicode(self.lan) + u' – ' + unicode(self.sponsor)

    class Meta:
        verbose_name = _(u'sponsor relation')
        verbose_name_plural = _(u'sponsor relations')
        ordering = ['-priority']
