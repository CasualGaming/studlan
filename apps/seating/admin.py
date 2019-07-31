# -*- coding: utf-8 -*-

from django.contrib import admin

from apps.seating.models import Layout, Seat, Seating


class SeatAdmin (admin.ModelAdmin):
    list_display = ('__unicode__', 'seating', 'user')
    list_filter = ('seating__lan',)
    search_fields = ['placement', 'user__username']


class SeatingAdmin (admin.ModelAdmin):
    pass


admin.site.register(Seating, SeatingAdmin)
admin.site.register(Seat, SeatAdmin)
admin.site.register(Layout)
