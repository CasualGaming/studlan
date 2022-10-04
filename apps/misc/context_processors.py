# -*- coding: utf-8 -*-

from django.conf import settings
from django.contrib.sites.models import Site


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
        'site_host': Site.objects.get_current().domain,
        'app_version': getattr(settings, 'VERSION', ''),
        'support_mail': getattr(settings, 'SUPPORT_MAIL', ''),
        'stripe_public_key': getattr(settings, 'STRIPE_PUBLIC_KEY', ''),
        'plausible_enable': getattr(settings, 'PLAUSIBLE_ENABLE', ''),
        'plausible_local_domain': getattr(settings, 'PLAUSIBLE_LOCAL_DOMAIN', ''),
        'plausible_remote_domain': getattr(settings, 'PLAUSIBLE_REMOTE_DOMAIN', ''),
        'full_app_name': build_full_app_name,
    }
