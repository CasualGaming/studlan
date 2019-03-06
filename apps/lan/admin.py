# -*- coding: utf-8 -*-

from django.conf import settings
from django.contrib import admin

from apps.lan.models import Directions, LAN, LANTranslation, Stream, Ticket, TicketType, TicketTypeTranslation


class LANTranslationInlineAdmin(admin.StackedInline):
    verbose_name = 'Translation'
    verbose_name_plural = 'Translations'
    model = LANTranslation
    max_num = len(settings.LANGUAGES)
    extra = 2


class LANAdmin(admin.ModelAdmin):
    model = LAN
    list_display = ['title', 'location', 'start_date', 'end_date']
    inlines = [LANTranslationInlineAdmin]


class TicketTypeTranslationInlineAdmin(admin.StackedInline):
    verbose_name = 'Translation'
    verbose_name_plural = 'Translations'
    model = TicketTypeTranslation
    max_num = len(settings.LANGUAGES)
    extra = 2


class TicketTypeAdmin(admin.ModelAdmin):
    model = TicketType
    inlines = [TicketTypeTranslationInlineAdmin]
    list_display = ['__unicode__', 'lan', 'number_of_seats', 'price']


class TicketAdmin(admin.ModelAdmin):
    model = Ticket
    list_display = ['__unicode__', 'ticket_type', 'bought_date']


admin.site.register(LAN, LANAdmin)
admin.site.register(TicketType, TicketTypeAdmin)
admin.site.register(Ticket, TicketAdmin)
admin.site.register(Directions)
admin.site.register(Stream)
