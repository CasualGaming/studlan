# -*- coding: utf-8 -*-

from django.contrib import admin

from studlan.lan.models import LAN

class LANAdmin(admin.ModelAdmin):
    model = LAN
    list_display = ['title', 'location', 'start_date', 'end_date',]

admin.site.register(LAN, LANAdmin)
