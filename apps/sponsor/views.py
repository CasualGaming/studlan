#!/usr/bin/python
# -*- coding: utf-8 -*-

from apps.sponsor.models import Sponsor
from django.shortcuts import render


def index(request):
    sponsors = Sponsor.objects.all()

    return render(request, 'sponsor/sponsors.html', {'sponsors': sponsors})