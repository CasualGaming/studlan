# -*- coding: utf-8 -*-

from django.conf import settings
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _lazy

from apps.sponsor.models import Sponsor, SponsorRelation, SponsorTranslation


class SponsorTranslationInlineAdmin(admin.StackedInline):
    verbose_name = _lazy(u'Translation')
    verbose_name_plural = _lazy(u'Translations')
    model = SponsorTranslation
    max_num = len(settings.LANGUAGES)
    extra = 2


class SponsorAdmin(admin.ModelAdmin):
    model = Sponsor
    list_display = ['title', 'website']
    inlines = [SponsorTranslationInlineAdmin]


class SponsorRelationAdmin(admin.ModelAdmin):
    model = SponsorRelation


admin.site.register(Sponsor, SponsorAdmin)
admin.site.register(SponsorRelation, SponsorRelationAdmin)
