# -*- coding: utf-8 -*-

from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class Config(AppConfig):
    name = 'apps.competition'
    verbose_name = _('Competition')
