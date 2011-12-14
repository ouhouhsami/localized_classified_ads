from functools import wraps
from django.contrib.sites.models import Site
from models import *
from forms import *
from filtersets import *

PER_SITE_OBJECTS = {
    'AcheterSansCom':{'ad_model':HomeForSaleAd, 'ad_form': HomeForSaleAdForm, 'ad_filterset':HomeForSaleAdFilterSet},
    'LouerSansCom':{'ad_model':HomeForRentAd, 'ad_form': HomeForRentAdForm, 'ad_filterset':HomeForRentAdFilterSet},
}

def site_decorator(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        current_site = Site.objects.get_current()
        kwargs['Ad'] = PER_SITE_OBJECTS[current_site.name]['ad_model']
        kwargs['AdForm'] = PER_SITE_OBJECTS[current_site.name]['ad_form']
        kwargs['AdFilterSet'] = PER_SITE_OBJECTS[current_site.name]['ad_filterset']
        return f(*args, **kwargs)
    return wrapper