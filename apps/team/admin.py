# -*- coding: utf-8 -*-

from django.contrib import admin

from apps.team.models import Invitation, Team


admin.site.register(Team)
admin.site.register(Invitation)
