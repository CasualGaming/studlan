# -*- coding: utf-8 -*-

from django.contrib import admin

from .models import Mail, MailRecipient


class MailAdmin(admin.ModelAdmin):

    list_display = ['uuid', 'subject', 'language', 'created_time', 'sender', 'is_sending_finished']
    ordering = ['-created_time']

    # Prevent creation
    def has_add_permission(self, request, obj=None):
        return False

    # Prevent deletion
    def has_delete_permission(self, request, obj=None):
        return False

    # Prevent changes
    def save_model(self, request, obj, form, change):
        pass

    # Prevent M2M changes
    def save_related(self, request, form, formsets, change):
        pass


class MailRecipientAdmin(admin.ModelAdmin):

    list_display = ['mail', 'user', 'sent_time']
    ordering = ['-sent_time']

    # Prevent creation
    def has_add_permission(self, request, obj=None):
        return False

    # Prevent deletion
    def has_delete_permission(self, request, obj=None):
        return False

    # Prevent changes
    def save_model(self, request, obj, form, change):
        pass

    # Prevent M2M changes
    def save_related(self, request, form, formsets, change):
        pass


admin.site.register(Mail, MailAdmin)
admin.site.register(MailRecipient, MailRecipientAdmin)
