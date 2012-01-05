#-*- coding: utf-8 -*-
from version import get_version

def localized_classified_ads_context_processor(request):
    results = {}
    results["version"] = get_version()
    return results