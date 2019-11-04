# -*- coding: utf-8 -*-

from django.contrib import admin

from apps.payment.models import LANTicketPurchaseLock


class LANTicketPurchaseLockAdmin(admin.ModelAdmin):
    model = LANTicketPurchaseLock


admin.site.register(LANTicketPurchaseLock, LANTicketPurchaseLockAdmin)
