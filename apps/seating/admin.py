#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.contrib import admin
from django.conf import settings

from apps.seating.models import Seat, Seating, Layout

class SeatAdmin (admin.ModelAdmin):
    list_display = ('user', 'placement', 'is_empty')
    list_filter = ('seating',)
    search_fields = ['user__username']

class SeatingAdmin (admin.ModelAdmin):
    pass


admin.site.register(Seating, SeatingAdmin)
admin.site.register(Seat, SeatAdmin)
admin.site.register(Layout)