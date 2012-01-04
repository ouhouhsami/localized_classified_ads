from django.conf import settings
from ads.models import HomeForRentAd, format_search_resume
from ads.forms import HomeForRentAdForm
from ads.filtersets import HomeForRentAdFilterSet

settings.PER_SITE_OBJECTS['LouerSansCom'] = {'ad_model':HomeForRentAd, 'ad_form': HomeForRentAdForm, 'ad_filterset':HomeForRentAdFilterSet, 'format_search_resume':format_search_resume}
