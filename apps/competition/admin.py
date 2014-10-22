#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.contrib import admin
from django.conf import settings

from apps.competition.models import Activity, Competition, Participant, CompetitionTranslation

class CompetitionTranslationInlineAdmin(admin.StackedInline):
    verbose_name = "Competition"
    verbose_name_plural = "Competitions"
    model = CompetitionTranslation
    max_num = len(settings.LANGUAGES)
    extra = 2

class CompetitionAdmin(admin.ModelAdmin):
    inlines = [CompetitionTranslationInlineAdmin,]

admin.site.register(Activity)
admin.site.register(Competition, CompetitionAdmin)
admin.site.register(Participant)
