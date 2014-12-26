# -*- coding: utf-8 -*-

from django.db import models


class Sponsor(models.Model):
    name = models.CharField("name", max_length=50)
    description = models.TextField('description')
    banner = models.CharField('Banner url', max_length=100, blank=True,
        help_text='Use a mirrored image of at least a height of 150px.')
    logo = models.CharField('Logo url', max_length=100, blank=True,
        help_text='Use a mirrored image of at least a height of 150px.')
    website = models.URLField("website", max_length=200)
    priority = models.IntegerField("priority", 
        help_text="higher priority means closer to the top of the sponsor list.")
    
    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['priority']
