# -*- coding: utf-8 -*-

from django.contrib import admin

from apps.seating.models import Layout, Seat, Seating


class LayoutAdmin(admin.ModelAdmin):
    model = Layout
    list_display = ['title', 'description']


class SeatingAdmin(admin.ModelAdmin):
    model = Seating
    list_display = ['__unicode__', 'layout']
    list_filter = ['lan']


class SeatAdmin(admin.ModelAdmin):
    model = Seat
    list_display = ['__unicode__', 'user']
    list_filter = ['seating__lan']
    search_fields = ['=placement', 'user__username']


admin.site.register(Layout, LayoutAdmin)
admin.site.register(Seating, SeatingAdmin)
admin.site.register(Seat, SeatAdmin)
