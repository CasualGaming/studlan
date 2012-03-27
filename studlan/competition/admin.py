#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.contrib import admin
from competition.models import Activity, Competition, Participant

admin.site.register(Activity)
admin.site.register(Competition)
admin.site.register(Participant)
