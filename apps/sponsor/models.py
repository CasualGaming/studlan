# -*- coding: utf-8 -*-

from django.db import models


class Sponsor(models.Model):
    name = models.CharField("name", max_length=50)
    website = models.URLField("website", max_length=200)
    priority = models.IntegerField("priority", 
        help_text="higher priority means closer to the top of the sponsor list.")
    
    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['priority']
