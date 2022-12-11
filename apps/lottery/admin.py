# -*- coding: utf-8 -*-

from django.conf import settings
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from .models import Lottery, LotteryParticipant



class LotteryAdmin(admin.ModelAdmin):
    list_display = ['lan']


class LotteryParticipantAdmin(admin.ModelAdmin):
    model = LotteryParticipant


admin.site.register(LotteryParticipant, LotteryParticipantAdmin)
admin.site.register(Lottery, LotteryAdmin)
