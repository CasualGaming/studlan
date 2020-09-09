# -*- coding: utf-8 -*-

from django.conf import settings
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from .models import Poll, PollOption, PollParticipant, PollTranslation


class PollTranslationInlineAdmin(admin.StackedInline):
    verbose_name = _(u'poll translation')
    verbose_name_plural = _(u'poll translations')
    model = PollTranslation
    max_num = len(settings.LANGUAGES)
    extra = 1


class PollOptionInlineAdmin(admin.StackedInline):
    verbose_name = _(u'poll option')
    verbose_name_plural = _(u'poll options')
    model = PollOption
    extra = 1


class PollAdmin(admin.ModelAdmin):
    inlines = [PollTranslationInlineAdmin, PollOptionInlineAdmin]
    list_display = ['__unicode__', 'lan']


class PollParticipantAdmin(admin.ModelAdmin):
    model = PollParticipant
    readonly_fields = ['poll', 'user', 'option']


admin.site.register(Poll, PollAdmin)
admin.site.register(PollParticipant, PollParticipantAdmin)
