from functools import wraps
from django.contrib.sites.models import Site
from django.conf import settings

def site_decorator(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        current_site = Site.objects.get_current()
        kwargs['Ad'] = settings.PER_SITE_OBJECTS[current_site.name]['ad_model']
        kwargs['AdForm'] = settings.PER_SITE_OBJECTS[current_site.name]['ad_form']
        kwargs['AdFilterSet'] = settings.PER_SITE_OBJECTS[current_site.name]['ad_filterset']
        return f(*args, **kwargs)
    return wrapper