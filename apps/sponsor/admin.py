# -*- coding: utf-8 -*-

from django.conf import settings
from django.contrib import admin

from apps.sponsor.models import Sponsor, SponsorRelation, SponsorTranslation

class SponsorTranslationInlineAdmin(admin.StackedInline):
    verbose_name = "Translation"
    verbose_name_plural = "Translations"
    model = SponsorTranslation
    max_num = len(settings.LANGUAGES)
    extra = 2

class SponsorAdmin(admin.ModelAdmin):
    model = Sponsor
    list_display = ['title', 'website']
    inlines = [SponsorTranslationInlineAdmin,]

class SponsorRelationAdmin(admin.ModelAdmin):
	model = SponsorRelation	

admin.site.register(Sponsor, SponsorAdmin)
admin.site.register(SponsorRelation, SponsorRelationAdmin)