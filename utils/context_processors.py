#-*- coding: utf-8 -*-
from version import get_version
from django.contrib.sites.models import Site
from django.conf import settings


def localized_classified_ads_context_processor(request):
    """
    Context processor, used to return version number
    """
    results = {}
    results["version"] = get_version()
    return results


def google_analytics_context_processor(request):
    current_site = Site.objects.get_current()
    return settings.GOOGLE_ANALYTICS_ACCOUNTS[str(current_site)]


def site_specific_styles(request):
    current_site = Site.objects.get_current()
    return settings.SITE_SPECIFIC_STYLES[str(current_site)]
