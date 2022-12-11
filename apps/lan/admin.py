# -*- coding: utf-8 -*-

from django.conf import settings
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from apps.lan.models import Attendee, Directions, LAN, Stream, Ticket, TicketType


class LANAdmin(admin.ModelAdmin):
    model = LAN
    list_display = ['title', 'slug', 'location', 'start_date', 'end_date']


class AttendeeAdmin(admin.ModelAdmin):
    model = Attendee
    list_display = ['has_paid', 'arrived']



class TicketTypeAdmin(admin.ModelAdmin):
    model = TicketType
    list_display = ['lan', 'number_of_seats', 'price']


class TicketAdmin(admin.ModelAdmin):
    model = Ticket
    list_display = ['ticket_type', 'bought_date', 'user']
    list_filter = ('ticket_type__lan', 'ticket_type')


admin.site.register(LAN, LANAdmin)
admin.site.register(Attendee, AttendeeAdmin)
admin.site.register(TicketType, TicketTypeAdmin)
admin.site.register(Ticket, TicketAdmin)
admin.site.register(Directions)
admin.site.register(Stream)
