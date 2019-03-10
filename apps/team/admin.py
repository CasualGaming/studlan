# -*- coding: utf-8 -*-

from django.contrib import admin
from django.contrib.admin.options import ModelAdmin

from apps.team.models import Invitation, Team


class InvitationAdmin(ModelAdmin):
    def has_add_permission(self, request, obj=None):
        return False


admin.site.register(Team)
admin.site.register(Invitation, InvitationAdmin)
