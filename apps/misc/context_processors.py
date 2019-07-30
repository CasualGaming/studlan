# -*- coding: utf-8 -*-

from django.conf import settings


def global_variables(request):
    return {
        'site_name': getattr(settings, 'SITE_NAME', ''),
        'app_version': getattr(settings, 'VERSION', ''),
        'support_mail': getattr(settings, 'SUPPORT_MAIL', ''),
        'stripe_public_key': getattr(settings, 'STRIPE_PUBLIC_KEY', ''),
    }
