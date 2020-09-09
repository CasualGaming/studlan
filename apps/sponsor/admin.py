# -*- coding: utf-8 -*-

from django.conf import settings
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from apps.sponsor.models import Sponsor, SponsorRelation, SponsorRelationTranslation, SponsorTranslation


class SponsorTranslationInlineAdmin(admin.StackedInline):
    verbose_name = _(u'partner translation')
    verbose_name_plural = _(u'partner translations')
    model = SponsorTranslation
    max_num = len(settings.LANGUAGES)
    extra = 2


class SponsorAdmin(admin.ModelAdmin):
    model = Sponsor
    list_display = ['title', 'website']
    inlines = [SponsorTranslationInlineAdmin]


class SponsorRelationTranslationInlineAdmin(admin.StackedInline):
    verbose_name = _(u'partner relation translation')
    verbose_name_plural = _(u'partner relation translations')
    model = SponsorRelationTranslation
    max_num = len(settings.LANGUAGES)
    extra = 2


class SponsorRelationAdmin(admin.ModelAdmin):
    model = SponsorRelation
    list_display = ('__unicode__', 'priority')
    list_filter = ('lan',)
    search_fields = ['sponsor__title']
    inlines = [SponsorRelationTranslationInlineAdmin]


admin.site.register(Sponsor, SponsorAdmin)
admin.site.register(SponsorRelation, SponsorRelationAdmin)
