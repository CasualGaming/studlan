# -*- coding: utf-8 -*-

from django.db import models

from translatable.models import TranslatableModel, get_translation_model

from apps.lan.models import LAN


class Sponsor(TranslatableModel):
    title = models.CharField('name', max_length=50)
    banner = models.CharField('Banner url', max_length=100, blank=True,
                              help_text='Use a mirrored image of at least a height of 150px.')
    website = models.URLField('website', max_length=200)

    def __unicode__(self):
        return self.title


class SponsorTranslation(get_translation_model(Sponsor, 'Sponsor')):
    description = models.TextField('description')


class SponsorRelation(models.Model):
    lan = models.ForeignKey(LAN)
    sponsor = models.ForeignKey(Sponsor)
    priority = models.IntegerField('priority',
                                   help_text='higher priority means closer to the top of the sponsor list.')

    def __unicode__(self):
        return unicode(self.lan) + ' - ' + unicode(self.sponsor)

    class Meta:
        ordering = ['-priority']
