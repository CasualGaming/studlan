# -*- coding: utf-8 -*-

from django.contrib import admin
from django.conf import settings

from apps.lottery.models import Lottery, LotteryTranslation
from apps.lottery.models import LotteryParticipant


class LotteryTranslationInlineAdmin(admin.StackedInline):
    verbose_name = 'Translation'
    verbose_name_plural = 'Translations'
    model = LotteryTranslation
    max_num = len(settings.LANGUAGES)
    extra = 1


class LotteryAdmin(admin.ModelAdmin):
    inlines = [LotteryTranslationInlineAdmin]
    list_display = ['__unicode__', 'lan']


class LotteryParticipantAdmin(admin.ModelAdmin):
    model = LotteryParticipant


admin.site.register(LotteryParticipant, LotteryParticipantAdmin)
admin.site.register(Lottery, LotteryAdmin)
