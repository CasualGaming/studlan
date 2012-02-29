#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.contrib import admin
from competition.models import Activity, Competition, UserProfile, Team
class UserProfileAdmin(admin.ModelAdmin):
    exclude=("user",)

admin.site.register(Activity)
admin.site.register(Competition)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Team)
