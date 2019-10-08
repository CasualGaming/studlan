# -*- coding: utf-8 -*-

from django.conf import settings


def build_full_app_name():
    full_app_name = 'studlan'
    version = getattr(settings, 'VERSION', '')
    show_version = getattr(settings, 'SHOW_VERSION', False)
    if show_version:
        full_app_name += ' v' + version
    return full_app_name


def global_variables(request):
    return {
        'site_name': getattr(settings, 'SITE_NAME', ''),
        'app_version': getattr(settings, 'VERSION', ''),
        'support_mail': getattr(settings, 'SUPPORT_MAIL', ''),
        'stripe_public_key': getattr(settings, 'STRIPE_PUBLIC_KEY', ''),
        'full_app_name': build_full_app_name,
    }
