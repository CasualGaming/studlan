# -*- coding: utf-8 -*-

from django.contrib import admin

from apps.lan.models import LAN, TicketType

class LANAdmin(admin.ModelAdmin):
    model = LAN
    list_display = ['title', 'location', 'start_date', 'end_date',]


class TicketTypeAdmin(admin.ModelAdmin):
    model = TicketType
    list_display = ['title', 'lan', 'number_of_seats', 'price',]

admin.site.register(LAN, LANAdmin)
admin.site.register(TicketType, TicketTypeAdmin)
