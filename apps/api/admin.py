# -*- coding: utf-8 -*-

import uuid

from django.contrib import admin

from apps.api.models import Key


class KeyAdmin(admin.ModelAdmin):
    list_display = ['owner', 'content']

    def save_model(self, request, obj, form, change):
        if not change:
            obj.content = uuid.uuid1().hex
        obj.save()


admin.site.register(Key, KeyAdmin)
