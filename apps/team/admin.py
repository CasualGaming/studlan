# -*- coding: utf-8 -*-

from django.contrib import admin

from apps.team.models import Team, Invitation

admin.site.register(Team)
admin.site.register(Invitation)