# -*- coding: utf-8 -*-

from django.conf import settings
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from apps.sponsor.models import Sponsor, SponsorRelation



class SponsorAdmin(admin.ModelAdmin):
    model = Sponsor
    list_display = ['title', 'website']



class SponsorRelationAdmin(admin.ModelAdmin):
    model = SponsorRelation
    # list_display = ('priority')
    list_filter = ('lan',)
    search_fields = ['sponsor__title']


admin.site.register(Sponsor, SponsorAdmin)
admin.site.register(SponsorRelation, SponsorRelationAdmin)
