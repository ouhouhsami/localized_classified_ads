"""
achetersanscom urls.py

"""
from django.conf.urls.defaults import patterns, include, url
from django.views.generic.simple import redirect_to

from profiles.views import UserProfileDetailView
from sites.achetersanscom.ads.models import HomeForSaleAd, HomeForSaleAdSearch

urlpatterns = patterns('',
    ('^$', redirect_to, {'url': '/annonce/search/'}),
    url(r'^annonce/', include('sites.achetersanscom.ads.urls')),
    url(r'^accounts/(?P<slug>(?!signout|signup|signin)[\.\w]+)/$', 
            UserProfileDetailView.as_view(ad_model=HomeForSaleAd, 
                                          ad_search_model=HomeForSaleAdSearch),
                                    name='userena_profile_detail'),
    url(r'^', include('localized_classified_ads.urls')),
)
