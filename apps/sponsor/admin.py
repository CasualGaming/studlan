# -*- coding: utf-8 -*-

from django.contrib import admin

from apps.sponsor.models import Sponsor

class SponsorAdmin(admin.ModelAdmin):
    model = Sponsor
    list_display = ['name', 'priority', 'website']

admin.site.register(Sponsor, SponsorAdmin)
