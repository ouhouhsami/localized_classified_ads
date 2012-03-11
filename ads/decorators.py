# coding=utf-8
from functools import wraps

from django.conf import settings
from django.contrib.sites.models import Site


def site_decorator(f):
    """
    Decorator for specifying generic ad views
    """
    @wraps(f)
    def wrapper(*args, **kwargs):
        #print kwargs
        current_site = Site.objects.get_current()
        kwargs['Ad'] = settings\
                           .PER_SITE_OBJECTS[current_site.name]['ad_model']
        kwargs['AdForm'] = settings\
                           .PER_SITE_OBJECTS[current_site.name]['ad_form']
        kwargs['AdFilterSet'] = settings\
                           .PER_SITE_OBJECTS[current_site.name]['ad_filterset']
        return f(*args, **kwargs)
    return wrapper