# -*- coding: utf-8 -*-

from django.conf import settings
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from .models import Poll, PollOption, PollParticipant



class PollOptionInlineAdmin(admin.StackedInline):
    verbose_name = _(u'poll option')
    verbose_name_plural = _(u'poll options')
    model = PollOption
    extra = 1


class PollAdmin(admin.ModelAdmin):
    inlines = [PollOptionInlineAdmin]
    list_display = ['lan']


class PollParticipantAdmin(admin.ModelAdmin):
    model = PollParticipant
    readonly_fields = ['poll', 'user', 'option']


admin.site.register(Poll, PollAdmin)
admin.site.register(PollParticipant, PollParticipantAdmin)
