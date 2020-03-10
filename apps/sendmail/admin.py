# -*- coding: utf-8 -*-

from django.contrib import admin

from .models import Mail


class MailAdmin(admin.ModelAdmin):

    list_display = ['subject', 'sent_time', 'recipients_total', 'successful_mails', 'failed_mails', 'done_sending']
    ordering = ['-sent_time']

    # Prevent creation
    def has_add_permission(self, request, obj=None):
        return False

    # Prevent changes
    def save_model(self, request, obj, form, change):
        pass

    # Prevent M2M changes
    def save_related(self, request, form, formsets, change):
        pass


admin.site.register(Mail, MailAdmin)
