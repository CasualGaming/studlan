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

    def get_sponsored_lans(self):
        return LAN.objects.filter(sponsorrelation__sponsor=self)

    class Meta:
        verbose_name = _(u'partner')
        verbose_name_plural = _(u'partners')


class SponsorTranslation(get_translation_model(Sponsor, 'partner')):
    description = models.TextField(_(u'description'))

    class Meta:
        verbose_name = _(u'partner translation')
        verbose_name_plural = _(u'partner translations')


class SponsorRelation(TranslatableModel):
    lan = models.ForeignKey(LAN, verbose_name=_(u'LAN'))
    sponsor = models.ForeignKey(Sponsor, verbose_name=_(u'partner'))
    priority = models.IntegerField(_(u'priority'),
                                   help_text=_(u'Higher priority means closer to the top of the partner list.'))

    def __unicode__(self):
        return unicode(self.lan) + u' – ' + unicode(self.sponsor)

    class Meta:
        verbose_name = _(u'partner relation')
        verbose_name_plural = _(u'partner relations')
        ordering = ['-priority']


class SponsorRelationTranslation(get_translation_model(SponsorRelation, 'partner relation')):
    description = models.TextField(_(u'description'))

    class Meta:
        verbose_name = _(u'partner relation translation')
        verbose_name_plural = _(u'partner relation translations')
