# -*- coding: utf-8 -*-

from django.conf import settings
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from apps.competition.models import Activity, Competition, CompetitionTranslation, Match, Participant


class CompetitionTranslationInlineAdmin(admin.StackedInline):
    verbose_name = _(u'Competition')
    verbose_name_plural = _(u'Competitions')
    model = CompetitionTranslation
    max_num = len(settings.LANGUAGES)
    extra = 2


class CompetitionAdmin(admin.ModelAdmin):
    inlines = [CompetitionTranslationInlineAdmin]
    list_display = ['__unicode__', 'lan']
    if (not settings.CHALLONGE_INTEGRATION_ENABLED) or settings.CHALLONGE_API_USERNAME == '' or \
            settings.CHALLONGE_API_KEY == '':
        exclude = ('challonge_url', 'max_match_points', 'tournament_format')


class MatchAdmin(admin.ModelAdmin):
    list_display = ('matchid', 'get_p1', 'get_p2', 'state', 'get_compo', 'get_lan')


admin.site.register(Activity)
admin.site.register(Competition, CompetitionAdmin)
admin.site.register(Participant)
admin.site.register(Match, MatchAdmin)
