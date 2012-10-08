"""
achetersanscom urls.py

"""
from django.conf.urls.defaults import patterns, include, url
from django.views.generic.simple import redirect_to
from django.contrib.sitemaps import FlatPageSitemap, GenericSitemap

from profiles.views import UserProfileDetailView
from sites.achetersanscom.ads.models import HomeForSaleAd, HomeForSaleAdSearch


home_for_sale_info_dict = {
    'queryset': HomeForSaleAd.objects.filter(visible=True),
    'date_field': 'create_date',
}

sitemaps = {
    'flatpages': FlatPageSitemap,
    'homeforsaleads': GenericSitemap(home_for_sale_info_dict, priority=0.6),
}

urlpatterns = patterns('',
    ('^$', redirect_to, {'url': '/annonce/search/'}),
    url(r'^annonce/', include('sites.achetersanscom.ads.urls')),
    url(r'^accounts/(?P<slug>(?!signout|signup|signin)[\.\w]+)/$',
            UserProfileDetailView.as_view(ad_model=HomeForSaleAd,
                                          ad_search_model=HomeForSaleAdSearch),
                                    name='userena_profile_detail'),
    (r'^sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps}),
    url(r'^', include('localized_classified_ads.urls')),
)
