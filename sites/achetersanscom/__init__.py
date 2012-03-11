from django.conf import settings
from ads.models import HomeForSaleAd, format_search_resume
from ads.forms import HomeForSaleAdForm
from ads.filtersets import HomeForSaleAdFilterSet

settings.PER_SITE_OBJECTS['AcheterSansCom'] = {'site_name':'AcheterSansCom', 
                     'ad_model':HomeForSaleAd, 'ad_form': HomeForSaleAdForm, 
                     'ad_filterset':HomeForSaleAdFilterSet, 
                     'format_search_resume':format_search_resume}
