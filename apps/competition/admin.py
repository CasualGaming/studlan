#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.contrib import admin
from django.conf import settings

from apps.competition.models import Activity, Competition, Participant, CompetitionTranslation, Match


class CompetitionTranslationInlineAdmin(admin.StackedInline):
    verbose_name = "Competition"
    verbose_name_plural = "Competitions"
    model = CompetitionTranslation
    max_num = len(settings.LANGUAGES)
    extra = 2


class CompetitionAdmin(admin.ModelAdmin):
    inlines = [CompetitionTranslationInlineAdmin,]
    list_display = ['__unicode__', 'lan',]

class MatchAdmin(admin.ModelAdmin):
    list_display = ('matchid','get_p1','get_p2','state','get_compo', 'get_lan',)

admin.site.register(Activity)
admin.site.register(Competition, CompetitionAdmin)
admin.site.register(Participant)
admin.site.register(Match, MatchAdmin)
