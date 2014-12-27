from django import template
from django.conf import settings

register = template.Library()

@register.simple_tag
def site_name():
    return getattr(settings, "SITE_NAME", "")

@register.simple_tag
def stripe_public_key():
    return getattr(settings, "STRIPE_PUBLIC_KEY", "")
