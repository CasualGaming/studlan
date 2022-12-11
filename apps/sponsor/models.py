# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext_lazy as _


from apps.lan.models import LAN


class Sponsor(models.Model):
    title = models.CharField(_('name'), max_length=50)
    banner = models.CharField(_('banner URL'), max_length=100, blank=True,
                              help_text=_('Use a mirrored image of at least a height of 150px.'))
    website = models.URLField(_('website'), max_length=200)

    def __unicode__(self):
        return self.title

    def get_sponsored_lans(self):
        return LAN.objects.filter(sponsorrelation__sponsor=self)

    class Meta:
        verbose_name = _('partner')
        verbose_name_plural = _('partners')



class SponsorRelation(models.Model):
    lan = models.ForeignKey(LAN, verbose_name=_('LAN'), on_delete=models.CASCADE)
    sponsor = models.ForeignKey(Sponsor, verbose_name=_('partner'), on_delete=models.CASCADE)
    priority = models.IntegerField(_('priority'),
                                   help_text=_('Higher priority means closer to the top of the partner list.'))

    def __unicode__(self):
        return str(self.lan) + ' – ' + str(self.sponsor)

    class Meta:
        verbose_name = _('partner relation')
        verbose_name_plural = _('partner relations')
        ordering = ['-priority']
