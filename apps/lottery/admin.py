# -*- coding: utf-8 -*-

from django.conf import settings
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from .models import Lottery, LotteryParticipant, LotteryTranslation


class LotteryTranslationInlineAdmin(admin.StackedInline):
    verbose_name = _(u'Translation')
    verbose_name_plural = _(u'Translations')
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
